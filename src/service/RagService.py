import util.qdrantServer as QS
from langchain_core.documents import Document
from pypdf import PdfReader

server = QS.getServerModel('teste')


# Função para treinar IA com PDF
def treinarArquivo(arquivo: str):
    try:
        vector = QS.vectorStore(server)

        with open(arquivo, 'rb') as pdf:
            reader = PdfReader(pdf)
            docs = []
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue
                doc = Document(
                    page_content=text,
                    metadata={
                        "source": arquivo,
                        "page": page_num
                    }
                )
                docs.append(doc)
        if not docs:
            print('Documento vazio!')
            return
        vector.add_documents(documents=getChunks(docs, server['chunkModel']['size'], server['chunkModel']['overlap']))
        print('Arquivo enviado para treinamento!')
    except Exception as e:
        print(e)


def getChunks(texto, size=1000, overlap=200):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    document_splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    chunks = document_splitter.split_documents(texto)

    return chunks
