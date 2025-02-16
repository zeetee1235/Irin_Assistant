import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_ollama import OllamaLLM
from langchain.schema import HumanMessage, AIMessage
import tkinter as tk
from tkinter import scrolledtext



def record_audio(duration=5, samplerate=44100, filename="voice.wav"): 
    #녹음시작
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    wav.write(filename, samplerate, audio_data)
    #음성파일 저장완료


def transcribe_audio(filename="voice.wav"):
    model = whisper.load_model("small").to("cuda") 
    # 모델크기 조절 (tiny, base, small, medium, large)
    # gpu 사용시 NVDA: .to("cuda")  AMD: .to("hip")  MAC: .to("mps")
    # CPU 강제사용 : .to("cpu")
    # 정밀도 연산 끝에 .half() 추가
    result = model.transcribe(filename)
    print("변환된 텍스트:", result["text"])
    return result["text"]



#llm 관련변수
Irin = OllamaLLM(model="irin")
chat_memory_list = []
chat_memory_CBM= ConversationBufferMemory(llm = Irin) #전체기억 메모리
questsion_number = 0
conversationchain = 0



#메모리 가공
def create_questsion_data(input,output):
    global questsion_number
    response_data = {
        "input": input,
        "output": output
    }
    return response_data

#메모리 제거
def remove_memory():
    global chat_memory_list
    if chat_memory_list.count == 100:
        message_to_remove_human = HumanMessage(content = chat_memory_list[0]["input"])
        chat_memory_list.pop(0)
        conversationchain.chat_memory.messages.remove[message_to_remove_human]

#프롬프트 메모리 저장
def save_memory(input_memory_list):
    global chat_memory_CBM
    x = input_memory_list["input"]
    y = input_memory_list["output"]
    chat_memory_CBM.save_context({"input": x}, {"output": y})
    

def clear_all_memory():
    x=x

#대화체인 생성
def generate_conversationchain():
    global conversationchain
    conversationchain = ConversationChain(
        llm = Irin,
        memory = ConversationBufferMemory()
    ) #conversationchain 대문자 소문자 주의


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


def ask_Irin(user_quest): #단순질문 앞에 대화체인을 먼저 생성해 놔야함
    global chat_memory_list
    global conversationchain
    answer_data = conversationchain.predict(input=user_quest)
    irin_answer = answer_data
    memory_data = create_questsion_data(user_quest,answer_data)
    chat_memory_list.append(memory_data)
    remove_memory()
    return irin_answer



# GUI 창 생성
window = tk.Tk()
window.title("Irin")
window.geometry("1000x800")

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
        response = ask_Irin(message)
        
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

generate_conversationchain()
# GUI 루프 시작
window.mainloop()



def test():
    run_Irin()


#test()