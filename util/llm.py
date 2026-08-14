import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def googleLLM():
    return GoogleGenerativeAI(model='gemini-3.1-flash-lite', google_api_key=API_KEY)

def googleEmbedding(model = 'gemini-embedding-001'):
    return GoogleGenerativeAIEmbeddings(model=model)

def ollamaEmbedding():
    return OllamaEmbeddings(model="nomic-embed-text")

def llmEmbedding(model = 'gemini'):
    if model == 'gemini':
        return googleEmbedding()
    if model == 'ollama':
        return ollamaEmbedding()