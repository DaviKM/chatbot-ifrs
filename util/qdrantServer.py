from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
import util.llm as llm

client = QdrantClient('http://localhost:6333')


def getServerModel(collection = 'teste'):
    embedding = llm.googleEmbedding()
    size = len(embedding.embed_query(collection))
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
        "embedding": embedding,
        "chunkModel": {'size': 500, 'overlap': 200}
    }


def vectorStore(serverModel):
    return QdrantVectorStore(
        client=serverModel['client'],
        collection_name=serverModel['collection'],
        embedding=serverModel['embedding']
    )
