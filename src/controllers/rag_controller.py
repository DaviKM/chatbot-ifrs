from fastapi import APIRouter, UploadFile, File
from src.service.rag_service import treinarArquivo
import os

router = APIRouter(prefix='/treinar', tags=['Treinar', 'IA', 'PDF'])

@router.post('')
async def treinarArquivo(arquivo: UploadFile = File()):
    try:
        path = os.path.join("src", "controllers", "uploads", arquivo.filename)
        with open(path, 'wb') as f:
            arquivo = await arquivo.read()
            f.write(arquivo)
        return 'Upload your file'
    except Exception as e:
        return e
    response = treinarArquivo(path)
    return response