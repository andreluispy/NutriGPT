import openai
import PySimpleGUI as sg

# API CONFIG
openai.api_key = ''
messages = []

# WINDOW CONFIG
layout = [
    [sg.Text("Massa: "), sg.Input(key='-massa-')],
    [sg.Text("Altura: "), sg.Input(key='-altura-')],
    [sg.Text("Digite suas Intolerancias: "), sg.Input(key='-intolerancia-')],
    [sg.Text('Objetivos'), sg.DropDown(['Uma Dieta Saudável', 'Ganhar Massa', 'Perder Peso'], key='-objetivo-')],
    [sg.Button('Send')]
]
window = sg.Window("NutriGPT", layout)

def getResponse(msg):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED:
        break
    elif event == "-send-":
        massa = 60
        tamanho = 1,60
        intolerancias = "O paciente não tem intolerância e nem alergia a nada"
        objetivo = "Uma Dieta saudável"
        
        question = f"Gere um plano alimentar para um paciente, seguindo as seguintes regras: 1. O paciente tem {massa} kg e {tamanho} metros; 2. Deve-se seguir o Guia Alimentar Brasileiro para criar o plano alimentar; 3. {intolerancias}; 4. O objetivo do plano alimentar é {objetivo} para o paciente; 5. Lembre-se de fornecer observações e dicas ao paciente"

        # Enviar Para o CHATGPT
        messages.append({"role": "user", "content": question})
        answer = getResponse(messages)
        
        print("ChatGPT:", answer[0], "\nCusto:\n", answer[1])
        messages.append({"role": "assistant", "content": answer[0]}) # Salvar Resposta do ChatGPT para conseguir contexto

window.close()
log = open('log.txt', 'w', encoding='utf-8') # UTF-8
log.write(str(messages).replace('\\n', '\n')) # \n
log.close()
