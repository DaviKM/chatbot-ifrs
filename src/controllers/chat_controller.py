from fastapi import APIRouter, Body
from src.service.rag_service import query
from database.db import Session
from database.model import Mensagem

router = APIRouter(prefix="/query", tags=["Query", "Search", "Chat"])

@router.post('')
def ask(pergunta : str = Body(embed=True)):
    """
    Endpoint para realizar uma consulta de pergunta e resposta.

    Args:
        pergunta (str): A pergunta a ser respondida.

    Returns:
        dict: Um dicionário contendo a resposta gerada.
    """
    resposta = query(pergunta, '51995361677')
    with Session() as session:
        mensagem = Mensagem(tel_n='51995361677', question=pergunta, answer=resposta)
        session.add(mensagem)
        session.commit()
    return {"resposta": resposta}