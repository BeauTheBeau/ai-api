# AI API
This is a simple API that allows you to use a combination of different methods to deliver GPT text generation.

## Installation
```bash
git clone https://github.com/beauthebeau/ai-api.git
pip install -r requirements.txt
# Also see https://pytorch.org/get-started/locally/
```

## Usage
```bash
python main.py # Starts the Uvicorn server
```

## Endpoints

### What is returned
All endpoints return the following:
```json
{
    "text": "The generated text"
}
```



### v1 routes

#### GET /generate/{prompt}
Generates text based on the prompt provided.
No context is provided, so the model will generate text based on the prompt only.
Returns a JSON object with the generated text. 


#### GET /generate/{prompt}/{context}
Generates text based on the prompt and context provided.
The context is provided as a string, and the model will generate text based on the prompt and context.
Returns a JSON object with the generated text. 


### v2 routes

Uses [DialoGPT](https://huggingface.co/microsoft/DialoGPT-medium), by Microsoft and trained on Reddit data to generate 
text. These routes use HuggingFace Transformers.

#### GET /generate/v2/?prompt={prompt}
Generates text based on the prompt provided.
No context is provided, so the model will generate text based on the prompt only.


### v3 routes

Uses OneAI's GPT Skill to generate text. The default model is [`text-davinci-003`](https://platform.openai.com/docs/models/gpt-3-5).
Note that this is a legacy model, superseded by `gpt-3.5-turbo`

#### GET /generate/v3/?prompt={prompt}
Generates text based on the prompt provided.
No context is provided, so the model will generate text based on the prompt only.


#### GET /generate/v3/?prompt={prompt}&context={context}
Generates text based on the prompt and context provided.
The context is provided as a string, and the model will generate text based on the prompt and context.


#### GET /generate/v3/?prompt={prompt}&preprompt={preprompt}&context={context}
Generates text based on the prompt, preprompt and context provided.
This is intended for when you're in a conversation with the AI, and you want to provide the previous prompt as well.
The context is provided as a string, and the model will generate text based on the prompt, preprompt and context.

