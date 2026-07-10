from fastapi import APIRouter, UploadFile
from src.service.rag_service import treinarArquivo

router = APIRouter(prefix='/treinar', tags=['Treinar', 'IA', 'PDF'])

@router.post('')
def treinarArquivo(file: UploadFile):
    path = file.filename
    response = treinarArquivo(path)
    return response