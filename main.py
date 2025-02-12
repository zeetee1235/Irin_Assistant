import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain_ollama import OllamaLLM


Iris = OllamaLLM(model="Iris")
chat_memory_list = []
chat_memory_CBM_list = ConversationBufferMemory(llm = Iris) #전체기억 메모리
chat_memory_CSM_list = ConversationSummaryMemory(llm = Iris) #요약기억 메모리
questsion_number = 0
conversation = 0



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


def ask_LLM(question):
    answer = conversation.predict(input = question)
    return answer


def create_questsion_data(input,output):
    global questsion_number
    response_data = {
        "input": input,
        "output": output
    }
    return response_data


def organize_memory():
    global chat_memory_list
    global chat_memory_CBM_list
    global chat_memory_CSM_list
    
    if chat_memory_CBM_list.count > 50:
        chat_memory_CSM_list.save_context({"input": chat_memory_list[50]["input"]}, {"output": chat_memory_list[50]["output"]})
        del chat_memory_CBM_list.chat_memory.messages[0]

    if chat_memory_CSM_list.count > 150:
        del chat_memory_CSM_list.chat_memory.messages[0]
    
    if chat_memory_list.count > 200:
        chat_memory_list.pop(0)

def save_memory(memory_list):
    cbm = ConversationBufferMemory(llm=Iris)
    x = memory_list["input"]
    y = memory_list["output"]
    cbm.save_context({"input": x}, {"output": y})
    

def clear_all_memory():
    x=x


def change_memory_CBM_to_CSM(x):
    x=x


def generate_conversationchain():
    global conversation
    conversation = ConversationChain(
        llm = Iris,
        memory = ConversationBufferMemory()
    )


def run_Iris():
    global chat_memory_list
    while True:
        user_input = input("질문 입력 (종료: exit): ")
        if user_input.lower() == "exit":
            break
        answer = Iris(user_input)
        base_memory_data = create_questsion_data(user_input,answer)
        chat_memory_list.append(base_memory_data)
        print("Iris:", answer)


def colligate(x):
    x=x


def test():
    run_Iris()


test()