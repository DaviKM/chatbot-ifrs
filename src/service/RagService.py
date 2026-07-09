import util.qdrantServer as QS
from langchain_community.document_loaders import PyPDFLoader

server = QS.getServerModel('teste')

# Função para treinar IA com PDF
def treinarArquivo(arquivo):
    vector = QS.vectorStore(server)

    loader = PyPDFLoader(f"./{arquivo}")
    docs = loader.load()

