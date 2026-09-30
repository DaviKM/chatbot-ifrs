import os
from fastapi import FastAPI


def create_app():
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from src.controllers.auth_controller import router as auth_router
    from src.controllers.rag_controller import router as rag_router
    from src.controllers.chat_controller import router as chat_router
    from database.db import Base, engine
    import database.model

    try:
        Base.metadata.create_all(engine)
        from src.service.auth_service import init_admin_user
        init_admin_user()
    except Exception as e:
        print(f"[DB] Aviso: Não foi possível conectar ao banco de dados na inicialização ({e}). O sistema continuará com autenticação padrão.")

    app = FastAPI(title="Chatbot IFRS API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ou ["*"] para liberar geral (cuidado em produção)
        allow_credentials=True,
        allow_methods=["*"],  # ou especificar: ["GET", "POST", "OPTIONS"]
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(rag_router)
    app.include_router(chat_router)

    return app

