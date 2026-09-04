import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY", None)
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')

def googleLLM():
    return GoogleGenerativeAI(model='gemini-3.1-flash-lite', google_api_key=API_KEY)

def googleEmbedding(model = 'gemini-embedding-001'):
    return GoogleGenerativeAIEmbeddings(model=model)

def ollamaLLM():
    return ChatOllama(model="gemma4", base_url=OLLAMA_URL)

def ollamaEmbedding():
    return OllamaEmbeddings(model="embeddinggemma",
                            base_url=OLLAMA_URL)

def llm(model = 'ollama'):
    if model == 'gemini':
        return googleLLM()
    if model == 'ollama':
        return ollamaLLM()

def llmEmbedding(model = 'gemini'):
    if model == 'gemini':
        return googleEmbedding()
    if model == 'ollama':
        return ollamaEmbedding()