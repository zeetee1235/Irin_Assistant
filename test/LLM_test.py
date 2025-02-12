import requests
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


Iris = OllamaLLM(model="Iris")
memory = ConversationBufferMemory(llm = "Iris")
conversation = 0

def ask_LLM(x):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "Iris",
        "prompt": x,
        "stream": False
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "No response from model.")
    else:
        return f"Error: {response.status_code}"


def generate_conversationchain():
    global conversation
    global memory
    conversation = ConversationChain(
        llm = Iris,
        memory = memory
    )


while True:
    generate_conversationchain()
    user_input = input("질문 입력 (종료: exit): ")
    if user_input.lower() == "exit":
        break
    answer = conversation.predict(input=user_input)
    print(answer)