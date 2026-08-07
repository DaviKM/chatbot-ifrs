import util.qdrant_server as QS
from util.log import writeLog
from langchain_core.documents import Document
from pypdf import PdfReader
from langchain_core.messages import HumanMessage, SystemMessage

server = QS.getServerModel('teste')


# Função para treinar IA com PDF
def treinarArquivo(arquivo: str, nomeArquivo: str):
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
                        "source": nomeArquivo,
                        "page": page_num
                    }
                )
                docs.append(doc)
            chunks = getChunks(docs, server['chunkModel']['size'], server['chunkModel']['overlap'])
            vector.add_documents(chunks)
        writeLog('RAG', 'INFO', 'Arquivo enviado para treinamento com sucesso', {
            "arquivo": nomeArquivo,
            "paginas": len(reader.pages)
        })
        return 'Arquivo enviado para treinamento!'
    except Exception as e:
        writeLog('RAG', 'ERROR', 'Ocorreu um erro ao tentar enviar o arquivo', {
            "arquivo": arquivo,
            "paginas": len(reader.pages),
            "erro": {
                'tipo': type(e).__name__,
                'mensagem': str(e),
            }
        })
        return str('Ocorreu um erro ao tentar enviar o arquivo')


def query(text: str):
    retriever = QS.getRetriever(server)
    docs = retriever.invoke(text)
    context = " ".join(doc.page_content for doc in docs)
    response = generation(text, context)
    writeLog('queries', 'INFO', 'Pergunta realizada', {
        "pergunta": text,
        "resposta": response
    })
    return response


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

# Só pra testes
# if __name__ == '__main__':
#  treinarArquivo('edital.pdf')
