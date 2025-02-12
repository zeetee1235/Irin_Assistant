import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_ollama import OllamaLLM
from langchain.schema import HumanMessage, AIMessage


Iris = OllamaLLM(model="Iris")
chat_memory_list = []
chat_memory_CBM= ConversationBufferMemory(llm = Iris) #전체기억 메모리
questsion_number = 0
conversationchain = 0


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


def create_questsion_data(input,output):
    global questsion_number
    response_data = {
        "input": input,
        "output": output
    }
    return response_data


def remove_memory():
    global chat_memory_list
    if chat_memory_list.count == 100:
        message_to_remove_human = HumanMessage(content = chat_memory_list[0]["input"])
        chat_memory_list.pop(0)
        conversationchain.chat_memory.messages.remove[message_to_remove_human]


def save_memory(input_memory_list):
    global chat_memory_CBM
    x = input_memory_list["input"]
    y = input_memory_list["output"]
    chat_memory_CBM.save_context({"input": x}, {"output": y})
    

def clear_all_memory():
    x=x


def generate_conversationchain():
    global conversationchain
    conversationchain = ConversationChain(
        llm = Iris,
        memory = ConversationBufferMemory()
    )


def run_Iris():
    global chat_memory_list
    generate_conversationchain()
    while True:
        user_input = input("질문 입력 (종료: exit): ")
        if user_input.lower() == "exit":
            break
        answer = conversationchain.predict(input=user_input)
        memory_data = create_questsion_data(user_input,answer)
        chat_memory_list.append(memory_data)
        remove_memory()
        print("Iris:", answer)


def colligate(x):
    x=x


def test():
    run_Iris()


test()