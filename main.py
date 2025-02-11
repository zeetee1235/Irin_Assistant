import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain_community.llms import Ollama



Iris = Ollama(model="Iris")
chat_memory = []
chat_memory_CBM = []
chat_memory_CSM = []
questsion_number = 0
memory = ConversationBufferMemory(llm=Iris) #CBM 전체기억
sum_memory = ConversationSummaryMemory(llm=Iris) #CSM 요약기억
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
    global chat_memory
    global chat_memory_CBM
    global chat_memory_CSM
    if chat_memory.count == 250:
        chat_memory.pop(0)
    if chat_memory_CBM.count == 50:
        chat_memory_CBM.pop(0)
    if chat_memory_CSM.count == 150:
        chat_memory_CSM.pop(0)



def save_memory(memory_list):
    cbm = ConversationBufferMemory(llm=Iris)
    x = memory_list["input"]
    y = memory_list["output"]
    cbm.save_context({"input": x}, {"output": y})
    

def clear_all_memory():
    global chat_memory
    chat_memory = []


def change_memory_CBM(x):
    x=x


def change_memory_CSM(x):
    x=x



def generate_conversationchain():
    global conversation
    conversation = ConversationChain(
        llm = Iris,
        memory = memory
    )


def run_Iris():
    global chat_memory
    while True:
        user_input = input("질문 입력 (종료: exit): ")
        if user_input.lower() == "exit":
            break
        answer = ask_LLM(user_input)
        memory_data = create_questsion_data(user_input,answer)
        chat_memory.append(memory_data)
        print("Iris:", answer)


def colligate(x):
    x=x


def test():
    run_Iris()


test()