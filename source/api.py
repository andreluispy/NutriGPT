from flask import Flask
from flask import request
import openai

sessions = {} # When user login, the messages data is saved here

def getResponse(msg): # CHATGPT GET RESPONSE
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

app = Flask(__name__)

@app.route('/')
def home():
    return "Acess API IN /api/getresponse"

@app.route('/api/getresponse')
def getresponse():
    api_key = request.args.get("apikey")
    massa = request.args.get("massa")
    altura = request.args.get("altura")
    intolerancias = request.args.get("intolerancias")
    objetivo = request.args.get("objetivo")

    openai.api_key = api_key
    try:
        messages = sessions[api_key]
    except KeyError:
        sessions[api_key] = []
        messages = sessions[api_key]

    # Make the question with the data from API
    question = f"Gere um plano alimentar para um paciente, seguindo as seguintes regras: 1. O paciente tem {massa} kg e {altura} metros; 2. Deve-se seguir o Guia Alimentar Brasileiro para criar o plano alimentar; 3. {intolerancias}; 4. O objetivo do plano alimentar é {objetivo} para o paciente; 5. Lembre-se de fornecer observações e dicas ao paciente"

    # Send to ChatGPT
    messages.append({"role": "user", "content": question})
    answer = getResponse(messages)
    messages.append({"role": "assistant", "content": answer[0]}) # Save the answer from ChatGPT in the sessions to make a context for the next messages

    return answer

app.run()
