from util.qdrantServer import vectorStore

try:
    vector_store = vectorStore()
    print('Vetor criado com sucesso!')
except Exception as e:
    print(e)