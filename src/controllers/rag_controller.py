from fastapi import APIRouter, UploadFile, File, Body, Depends
from src.service.rag_service import treinarArquivo, delete, listar_arquivos
from src.service.auth_service import get_current_user
import os

router = APIRouter(prefix='/rag', tags=['Treinar', 'IA', 'PDF'])

@router.get('/arquivos')
def listar(current_user: dict = Depends(get_current_user)):
    try:
        arquivos = listar_arquivos("uploaded")
        return {"status": "sucesso", "arquivos": arquivos}
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")
        return {"status": "erro", "Erro": str(e), "arquivos": []}

@router.post('/treinar')
async def treinar(
    arquivo: UploadFile = File(),
    current_user: dict = Depends(get_current_user)
):
    try:
        os.makedirs("uploaded", exist_ok=True)
        path = os.path.join("uploaded", arquivo.filename)
        with open(path, 'wb') as f:
            content = await arquivo.read()
            f.write(content)
        response = treinarArquivo(path, arquivo.filename)
        print(response)
        return {"status": "sucesso", "mensagem": str(response), "arquivo": arquivo.filename}
    except Exception as e:
        print(e)
        return {"status": "erro", "Erro": str(e)}

@router.post('/deletar')
def deletar(
    nome_arquivo: str = Body(embed=True),
    current_user: dict = Depends(get_current_user)
):
    try:
        path = os.path.join("uploaded", nome_arquivo)
        delete(path, nome_arquivo)
        return {"status": "sucesso", "mensagem": f"Arquivo '{nome_arquivo}' deletado com sucesso!"}
    except Exception as e:
        print(e)
        return {"status": "erro", "Erro": str(e)}

@router.delete('/arquivo/{nome_arquivo}')
def deletar_por_parametro(
    nome_arquivo: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        path = os.path.join("uploaded", nome_arquivo)
        delete(path, nome_arquivo)
        return {"status": "sucesso", "mensagem": f"Arquivo '{nome_arquivo}' deletado com sucesso!"}
    except Exception as e:
        print(e)
        return {"status": "erro", "Erro": str(e)}

