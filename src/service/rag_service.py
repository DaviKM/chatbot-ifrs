import os.path

from qdrant_client.http.models import FilterSelector, Filter, FieldCondition, MatchValue
import util.qdrant_server as QS
from util.log import writeLog
from langchain_core.documents import Document
from pypdf import PdfReader
from langchain_core.messages import HumanMessage, SystemMessage
from util.llm import llm

server = QS.getServerModel(collection='ifrs', model='ollama', embeddingModel='ollama')

# Função para treinar IA com PDF
def treinarArquivo(arquivo: str, nomeArquivo: str):
    with open(arquivo, 'rb') as pdf:
        reader = PdfReader(pdf)
        try:
            vector = QS.vectorStore(server)
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


def query(text: str, tel):
    historico = getHistorico(tel)
    question = llm().invoke(
        f"Com base no histórico da conversa e na nova pergunta do usuário, gere uma única frase contendo palavras chaves de busca que represente a real intenção dele."
        f"O objetivo é procurar por informações em um banco de dados vetorial que contém informações de editais para o processo seletivo de uma instituição."
        f"Se não houver histórico de conversa ou a nova pergunta não tiver relação com as anteriores, apenas reescreva a pergunta para que a pesquisa fique"
        f"mais clara, mas sem alterar seu interesse realou incluindo informações que podem alterar o resultado final."
        f"\n\nHistórico de conversa: {historico}"
        f"\n\n Nova pergunta: {text}"
    )
    question = question.content if server['model'] == 'ollama' else question

    print(question)
    retriever = QS.getRetriever(server)
    docs = retriever.invoke(question)
    context = " ".join(doc.page_content for doc in docs)
    response = generation(text, context)
    writeLog('queries', 'INFO', 'Pergunta realizada', {
        "pergunta": text,
        "resposta": response
    })
    print(f'Pergunta do Usuário: {text}\n\nPergunta da IA: {question}\n\nBusca: {context}\n\nResposta: {response}')
    return response


def generation(hm, context):
    sm = (
        "Você é um assistente para tarefas de resposta a perguntas. "
        "Use as seguintes partes do contexto recuperado para responder a pergunta. "
        "Se você não sabe a resposta ou o contexto não foi passado, diga que "
        "o documento não fala sobre isso. Use no máximo três frases e mantenha a "
        "resposta concisa.\n\nContexto: {contexto}"
    ).format(contexto=context)
    print(sm)
    messages = [
        SystemMessage(content=sm),
        HumanMessage(content=hm)
    ]

    response = llm().invoke(messages)
    response = response.content if server['model'] == 'ollama' else response
    return response

def getHistorico(tel):
    from sqlalchemy import select
    from database.db import Session
    from database.model import Mensagem

    with Session() as session:
        stmt = select(Mensagem.question, Mensagem.answer, Mensagem.date).where(Mensagem.tel_n == tel).order_by(Mensagem.date.asc())
        response = session.execute(stmt).all()
        historico = ""
        for row in response:
            historico += f"Data: {row.date} \nPergunta: {row.question}\nResposta: {row.answer}\n\n"
        return historico

def getChunks(texto, size=1000, overlap=200):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    document_splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    chunks = document_splitter.split_documents(texto)

    return chunks

def delete(caminho : str, nome : str):
    try:
        client = server['client']
        colecao = server['collection']
        client.delete(
            collection_name=colecao,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key='metadata.source',
                            match=MatchValue(value=nome)
                        )
                    ]
                )
            )
        )
        if os.path.exists(caminho):
            os.remove(caminho)
        else:
            print('O arquivo não existe')
        writeLog('RAG', 'INFO', 'Arquivo deletado', {
            "arquivo": nome,
        })
        return 'Deletado com sucesso'
    except Exception as e:
        print(str(e))
        writeLog('RAG', 'ERROR', 'Falha ao deletar arquivo', {
            "arquivo": nome,
            "erro": {
                'tipo': type(e).__name__,
                'mensagem': str(e),
            }
        })
        return e
# Só pra testes
if __name__ == '__main__':
  delete('../../uploaded/EDITAL-No-12-2026-EDITAL-DO-PROCESSO-SELETIVO-DE-VAGAS-NAO-PREENCHIDAS-2026-2.pdf', 'EDITAL-No-12-2026-EDITAL-DO-PROCESSO-SELETIVO-DE-VAGAS-NAO-PREENCHIDAS-2026-2.pdf')
