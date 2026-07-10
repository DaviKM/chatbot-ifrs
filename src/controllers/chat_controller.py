from fastapi import APIRouter, Body
from src.service.rag_service import query
from src.models.chat import Chat

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
    resposta = query(pergunta)
    return {"resposta": resposta}