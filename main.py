from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import languagemodels as lm
import uvicorn
import os

app = FastAPI()
lm.set_max_ram('4g')


@app.get("/", response_class=HTMLResponse)
def read_root():
    # Return index.html
    with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'r') as f:
        return f.read()


# API endpoint for generating text with context
@app.get("/generate/{prompt}/{context}")
def generate(prompt: str, context: str):
    print("w/ context")
    text = lm.do(f"You have been provided the following context: {context} | Respond as helpfully as you can, "
                 f"remember to be very friendly| This is the user's prompt {prompt}")

    return {"text": text}


# API endpoint for generating text without context
@app.get("/generate/{prompt}")
def generate(prompt: str):
    print("w/o context")
    text = lm.do(f"Respond as helpfully as you can | Remember to be very friendly, greeting the user | This is the "
                 f"user's prompt {prompt}")
    return {"text": text}


import time
from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "microsoft/DialoGPT-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize chat history as an empty list
chat_history_ids = []

@app.get("/generate/v2/")
def generate_with_context(prompt: str):
    global chat_history_ids  # Use the global chat history variable

    text = prompt
    startTime = time.time()
    input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')

    # Generate the model's response
    response_ids = model.generate(
        input_ids,
        max_length=4096,
        do_sample=True,
        top_k=100,
        temperature=0.75,
        pad_token_id=tokenizer.eos_token_id
    )

    # Update the chat history with both the input and response
    chat_history_ids.extend(input_ids.tolist()[0])
    chat_history_ids.extend(response_ids.tolist()[0])

    # Decode the response and return
    output = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    print(f"BEE6: {output} ({time.time() - startTime:.2f}s)")
    return {"text": output}

# Run the API
if __name__ == "__main__":
    print("Running API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
