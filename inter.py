import tkinter as tk
from tkinter import scrolledtext
from langchain_ollama import OllamaLLM

# Ollama 모델 초기화
Irin = OllamaLLM(model="Irin")

# GUI 창 생성
window = tk.Tk()
window.title("Iris")
window.geometry("500x400")

# 대화 기록 표시 영역
chat_display = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='disabled')
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 사용자 입력 필드
user_input = tk.Entry(window, width=80)
user_input.pack(padx=10, pady=(0, 10), fill=tk.X)

def send_message(event=None):
    message = user_input.get()
    if message.strip():
        # 사용자 메시지 표시
        chat_display.configure(state='normal')
        chat_display.insert(tk.END, f"사용자: {message}\n")
        chat_display.configure(state='disabled')
        
        # LLM 응답 생성
        response = Irin(message)
        
        # LLM 응답 표시
        chat_display.configure(state='normal')
        chat_display.insert(tk.END, f"LLM: {response}\n\n")
        chat_display.configure(state='disabled')
        
        # 스크롤을 최신 메시지로 이동
        chat_display.yview(tk.END)
        
        # 입력 필드 초기화
        user_input.delete(0, tk.END)

# 엔터 키 이벤트 바인딩
user_input.bind("<Return>", send_message)

# GUI 루프 시작
window.mainloop()