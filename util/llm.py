import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def googleLLM():
    return GoogleGenerativeAI(model='gemini-3.1-flash-lite', google_api_key=API_KEY)

def googleEmbedding(model = 'gemini-embedding-001'):
    return GoogleGenerativeAIEmbeddings(model=model)