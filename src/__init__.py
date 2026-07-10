from fastapi import FastAPI

def create_app():
    from src.controllers.rag_controller import router as rag_router
    from src.controllers.chat_controller import router as chat_router

    app = FastAPI()

    app.include_router(rag_router)
    app.include_router(chat_router)

    return app