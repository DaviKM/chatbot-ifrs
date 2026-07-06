from util.llm import googleLLM

llm = googleLLM()

while True:
    pergunta = input('Pergunta: ')
    if pergunta == '':
        break
    print(llm.invoke(pergunta))