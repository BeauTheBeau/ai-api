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


# Run the API
if __name__ == "__main__":
    print("Running API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
