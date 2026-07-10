from fastapi import FastAPI


def create_app():
    from fastapi.middleware.cors import CORSMiddleware
    from src.controllers.rag_controller import router as rag_router
    from src.controllers.chat_controller import router as chat_router

    app = FastAPI()

    """origins = [
        "http://localhost:6060"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Allows specified origins
        allow_credentials=True,  # Allows cookies/auth headers
        allow_methods=["*"],  # Automatically responds to OPTIONS with allowed methods
        allow_headers=["*"],  # Allows all custom headers
    ) """

    app.include_router(rag_router)
    app.include_router(chat_router)

    return app
