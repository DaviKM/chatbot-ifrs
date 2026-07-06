import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def googleLLM():
    return GoogleGenerativeAI(model='gemini-3.5-flash', google_api_key=API_KEY)

