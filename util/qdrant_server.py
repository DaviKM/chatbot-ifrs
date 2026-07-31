import os

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
import util.llm as llm
from dotenv import load_dotenv

load_dotenv()

QDRANT_HOST = os.getenv('QDRANT_HOST', 'localhost')
QDRANT_PORT = int(os.getenv('QDRANT_PORT', '6333'))
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def getServerModel(collection = 'teste', model = 'gemini', size = 3072):
    if not client.collection_exists(collection):
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(
                size=size,
                distance=Distance.COSINE
            )
        )
    return {
        "client": client,
        "collection": collection,
        "model": model,
        "chunkModel": _defineChunks(model)
    }


def vectorStore(serverModel):
    return QdrantVectorStore(
        client=serverModel['client'],
        collection_name=serverModel['collection'],
        embedding=llm.llmEmbedding(serverModel['model'])
    )

def getRetriever(serverModel):
    vector_store = vectorStore(serverModel)
    retriever = vector_store.as_retriever(
        search_type='similarity_score_threshold',
        search_kwargs={'score_threshold': 0.8}
    )
    return retriever

def _defineChunks(model):
    base = {
        'gpt' : { 'size': 1000, 'overlap': 200},
        'gemini' : { 'size': 1000, 'overlap': 200}
    }

    return base[model]