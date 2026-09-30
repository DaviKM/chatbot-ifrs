import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

try:
    from util.hash import hash, verify_hash
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from util.hash import hash, verify_hash

# Configurações de JWT e Usuário Administrador Genérico
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "chatbot_ifrs_super_secret_jwt_key_2026_canoas_32bytes")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def init_admin_user():
    """
    Inicializa o usuário administrador genérico no banco de dados se ainda não existir.
    """
    try:
        from database.db import Session
        from database.model import Usuario
        from sqlalchemy import select

        with Session() as session:
            stmt = select(Usuario).where(Usuario.name == ADMIN_USERNAME)
            user = session.execute(stmt).scalar_one_or_none()
            if not user:
                admin_user = Usuario(
                    name=ADMIN_USERNAME,
                    hash=hash(ADMIN_PASSWORD)
                )
                session.add(admin_user)
                session.commit()
                print(f"[AUTH] Usuário admin genérico '{ADMIN_USERNAME}' cadastrado/sincronizado no banco de dados.")
    except Exception as e:
        print(f"[AUTH] Aviso ao inicializar admin no banco de dados: {e}. Usando credenciais padrão do ambiente.")


def authenticate_user(username: str, password: str) -> bool:
    """
    Autentica o usuário como admin genérico, verificando as credenciais no banco ou via variáveis de ambiente.
    """
    # 1. Verifica se bate diretamente com as credenciais do admin genérico configuradas no .env
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True

    # 2. Verifica se o usuário existe na tabela Usuario com a senha correspondente (hash.py)
    try:
        from database.db import Session
        from database.model import Usuario
        from sqlalchemy import select

        with Session() as session:
            stmt = select(Usuario).where(Usuario.name == username)
            user = session.execute(stmt).scalar_one_or_none()
            if user and verify_hash(password, user.hash):
                return True
    except Exception:
        pass

    return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Gera um novo token JWT codificado com tempo de expiração.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decodifica e valida o token JWT.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado. Por favor, autentique-se novamente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependência do FastAPI para proteger endpoints que exigem autenticação do admin.
    """
    payload = decode_access_token(token)
    username: Optional[str] = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: identidade do usuário não encontrada.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "username": username,
        "role": payload.get("role", "admin")
    }
