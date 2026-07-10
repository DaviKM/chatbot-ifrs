import uvicorn
from src import create_app

app = create_app()

@app.get('/')
def index():
    return {'Hello': 'World'}

print("App inicializado")
if __name__ == "__main__":
    uvicorn.run("main:app",
                #host="0.0.0.0",
                port=6000,
                reload=True)