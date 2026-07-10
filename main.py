import uvicorn
from src import create_app
app = create_app()

@app.get('/')
def index():
    return {'Hello': 'World'}

if __name__ == "__main__":
    uvicorn.run("main:app",
                #host="0.0.0.0",
                port=6060,
                reload=True)
    print("App inicializado")