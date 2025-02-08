import requests

def ask_deepseek(question):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "Iris",
        "prompt": question,
        "stream": False
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "No response from model.")
    else:
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    while True:
        user_input = input("질문을 입력하세요 (종료: exit): ")
        if user_input.lower() == "exit":
            break
        answer = ask_deepseek(user_input)
        print("답변:", answer)
