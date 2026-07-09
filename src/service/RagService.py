import util.qdrantServer as QS

try:
    server = QS.getServerModel('teste5')
    vector = QS.vectorStore(server)
    print('Criado com sucesso!')
except Exception as e:
    print('Erro:' + str(e))
