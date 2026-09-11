from fastapi import APIRouter, Body
from src.service.rag_service import query
from database.db import Session
from database.model import Mensagem
from sqlalchemy import select

router = APIRouter(prefix="/chat", tags=["Query", "Search", "Chat"])

@router.post('/query')
def ask(pergunta : str = Body(embed=True),
        tel: str = Body(embed=True)):
    """
    Endpoint para realizar uma consulta de pergunta e resposta.

    Args:
        pergunta (str): A pergunta a ser respondida.
        tel (str): O número de telefone do usuário.

    Returns:
        dict: Um dicionário contendo a resposta gerada.
    """
    resposta = query(pergunta, tel)
    with Session() as session:
        mensagem = Mensagem(tel_n=tel, question=pergunta, answer=resposta)
        session.add(mensagem)
        session.commit()
    return {"resposta": resposta}

@router.get('/historico/{tel}')
def get_historico(tel: str):
    """
    Endpoint para obter o histórico de perguntas e respostas de um determinado número de telefone.

    Args:
        tel (str): O número de telefone para o qual o histórico será obtido.

    Returns:
        list: Uma lista de dicionários contendo as perguntas, respostas e datas correspondentes.
    """
    with Session() as session:
        stmt = select(Mensagem.question, Mensagem.answer).where(Mensagem.tel_n == tel).order_by(Mensagem.date.asc())
        response = session.execute(stmt)
        result = response.mappings().all()
    return result