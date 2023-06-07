import openai

"""
METODOLOGIA _SEM NOME_ por André Luís Portela Neves
"""

openai.api_key = ''
messages = []

def getResponse(msg):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

while True:
    # Conseguir INPUT
    question = input(">> ")

    # Manipular o INPUT
    if question == "sair":
        break
    else:
        # Enviar Para o CHATGPT
        messages.append({"role": "user", "content": question})
        answer = getResponse(messages)
        
        print("ChatGPT:", answer[0], "\nCusto:\n", answer[1])
        messages.append({"role": "assistant", "content": answer[0]}) # Salvar Resposta do ChatGPT para conseguir contexto

log = open('log.txt', 'w', encoding='utf-8') # UTF-8
log.write(str(messages).replace('\\n', '\n')) # \n
log.close()
