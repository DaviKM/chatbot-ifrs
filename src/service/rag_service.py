import util.qdrant_server as QS
from langchain_core.documents import Document
from pypdf import PdfReader
from langchain_core.messages import HumanMessage, SystemMessage

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


def query(text : str):
    retriever = QS.getRetriever(server)
    docs = retriever.invoke(text)
    context = " ".join(doc.page_content for doc in docs)
    return generation(text, context)


def generation(hm, context):
    from util.llm import googleLLM
    sm = (
        "Você é um assistente para tarefas de resposta a perguntas. "
        "Use as seguintes partes do contexto recuperado para responder a pergunta. "
        "Se você não sabe a resposta ou o contexto não foi passado, diga que "
        "o documento não fala sobre isso. Use no máximo três frases e mantenha a "
        "resposta concisa.\n\n{contexto}"
    ).format(contexto=context)

    messages = [
        SystemMessage(content=sm),
        HumanMessage(content=hm)
    ]

    response = googleLLM().invoke(messages)
    return response


def getChunks(texto, size=1000, overlap=200):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    document_splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    chunks = document_splitter.split_documents(texto)

    return chunks

print(query("O que você sabe sobre a seleção Brasileira?"))