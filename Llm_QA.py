from llama_cpp import Llama

# Llama 모델 로드 (경로는 모델 위치 수정)
llm = Llama(model_path="C:/AI/models/llama-2-7b.Q4_0.gguf", n_ctx=2048)

def ask_llm(question):
    response = llm(question, max_tokens=200)
    return response["choices"][0]["text"].strip()

if __name__ == "__main__":
    while True:
        user_input = input("질문: ")
        if user_input.lower() in ["exit", "quit", "종료"]:
            print("프로그램을 종료합니다.")
            break
        answer = ask_llm(user_input)
        print("AI 응답:", answer)
