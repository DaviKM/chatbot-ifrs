from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
import util.llm as llm

client = QdrantClient('http://localhost:6333')

def vectorStore(nome = 'teste'):
    embedding = llm.googleEmbedding()
    size = len(embedding.embed_query(nome))
    if not client.collection_exists(nome):
        client.create_collection(
            collection_name=nome,
            vectors_config=VectorParams(
            size=size,
            distance=Distance.COSINE
            )
        )
    return QdrantVectorStore(
        client=client,
        collection_name=nome,
        embedding=llm.googleEmbeddings()
    )