import requests
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


Irin = OllamaLLM(model="Irin")
memory = ConversationBufferMemory(llm = "Irin")
conversationchain = 0

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
        llm = Irin,
        memory = memory
    )


while True:
    generate_conversationchain()
    user_input = input("질문 입력 (종료: exit): ")
    if user_input.lower() == "exit":
        break
    answer = conversation.predict(input=user_input)
    print(answer)


'''    
def run_Irin(): #반복 질문
    global chat_memory_list
    generate_conversationchain()
    while True:
        user_quest = input("질문 입력 (종료: exit): ")
        if user_quest.lower() == "exit":
            break
        answer = conversationchain.predict(input=user_quest)
        memory_data = create_questsion_data(user_quest,answer)
        chat_memory_list.append(memory_data)
        remove_memory()
        print("Iris:", answer)
'''