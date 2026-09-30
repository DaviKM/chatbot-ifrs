from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from src.service.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/auth", tags=["Autenticação", "Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=TokenResponse)
def login_json(credentials: LoginRequest):
    """
    Endpoint para autenticação de administrador via JSON (utilizado pela aplicação frontend).
    """
    if not authenticate_user(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": credentials.username, "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token", response_model=TokenResponse)
def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para autenticação via formulário OAuth2 (utilizado pelo Swagger UI em /docs).
    """
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": form_data.username, "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify")
@router.get("/me")
def verify_token(current_user: dict = Depends(get_current_user)):
    """
    Endpoint para verificar a validade do token JWT e retornar os dados do usuário autenticado.
    """
    return {
        "status": "authenticated",
        "user": current_user
    }
