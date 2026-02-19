from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# connect backend to frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class PromptRequest(BaseModel):
    userInput: str

@app.post('/generate', status_code=200)
def generate(request: PromptRequest):
    response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=f'Can you decide for the user what movie they should watch from the list they gave you, provide a synopsys for the movie and suggest a snack to go along with the movie {request.userInput}',
)
    return {'response': response.text}