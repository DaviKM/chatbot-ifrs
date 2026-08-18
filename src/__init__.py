from fastapi import FastAPI


def create_app():
    from fastapi.middleware.cors import CORSMiddleware
    from src.controllers.rag_controller import router as rag_router
    from src.controllers.chat_controller import router as chat_router
    from database.db import Base, engine
    import database.model

    Base.metadata.create_all(engine)

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ou ["*"] para liberar geral (cuidado em produção)
        allow_credentials=True,
        allow_methods=["*"],  # ou especificar: ["GET", "POST", "OPTIONS"]
        allow_headers=["*"],
    )

    app.include_router(rag_router)
    app.include_router(chat_router)

    return app
