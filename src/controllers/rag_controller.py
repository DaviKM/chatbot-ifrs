from fastapi import APIRouter, UploadFile, File
from src.service.rag_service import treinarArquivo
import os

router = APIRouter(prefix='/treinar', tags=['Treinar', 'IA', 'PDF'])

@router.post('')
async def treinar(arquivo: UploadFile = File()):
    try:
        path = os.path.join("uploaded", arquivo.filename)
        with open(path, 'wb') as f:
            file = await arquivo.read()
            f.write(file)
        response = treinarArquivo(path, arquivo.filename)
        print(response)
        return response
    except Exception as e:
        print(e)
        return {"Erro": e}
