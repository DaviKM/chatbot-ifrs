from fastapi import APIRouter, UploadFile, File, Body, Depends
from src.service.rag_service import treinarArquivo, delete
from src.service.auth_service import get_current_user
import os

router = APIRouter(prefix='/rag', tags=['Treinar', 'IA', 'PDF'])

@router.post('/treinar')
async def treinar(
    arquivo: UploadFile = File(),
    current_user: dict = Depends(get_current_user)
):
    try:
        path = os.path.join("uploaded", arquivo.filename)
        with open(path, 'wb') as f:
            content = await arquivo.read()
            f.write(content)
        response = treinarArquivo(path, arquivo.filename)
        print(response)
        return response
    except Exception as e:
        print(e)
        return {"Erro": str(e)}

@router.post('/deletar')
def deletar(
    nome_arquivo: str = Body(embed=True),
    current_user: dict = Depends(get_current_user)
):
    try:
        path = os.path.join("uploaded", nome_arquivo)
        delete(path, nome_arquivo)
        return "Deletado com sucesso!"
    except Exception as e:
        print(e)
        return {"Erro": str(e)}

