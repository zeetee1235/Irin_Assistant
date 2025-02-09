import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.llms import Ollama



Iris = Ollama(model="Iris")
chat_memory = ()
questsion_number = 0
memory = ConversationBufferMemory(llm=Iris) #전체기억
conversation = 0



def record_audio(duration=5, samplerate=44100, filename="voice.wav"): 
    print("녹음 시작")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    wav.write(filename, samplerate, audio_data)
    print("녹음 완료 파일 저장됨:", filename)


def transcribe_audio(filename="voice.wav"):
    model = whisper.load_model("small").to("cuda") 
    # 모델크기 조절 (tiny, base, small, medium, large)
    # gpu 사용시 NVDA: .to("cuda")  AMD: .to("hip")  MAC: .to("mps")
    # CPU 강제사용 : .to("cpu")
    # 정밀도 연산 끝에 .half() 추가
    result = model.transcribe(filename)
    print("변환된 텍스트:", result["text"])
    return result["text"]


def ask_LLM(x):
    answer = conversation.predict(input = x)
    return answer


def create_questsion_data(x,y):
    global questsion_number
    response_data = {
        "text": x,
        "number": questsion_number
    }
    questsion_number = questsion_number + 1
    return response_data


def organize_memory(x):
    x=x

def clear_memory(x):
    x=x


def generate_conversationchain():
    global conversation
    conversation = ConversationChain(
        llm = Iris,
        memory = memory
    )


def run_Iris():
    generate_conversationchain()
    while True:
        user_input = input("질문 입력 (종료: exit): ")
        if user_input.lower() == "exit":
            break
        answer = ask_LLM(user_input)
        print("Iris:", answer)


def colligate(x):
    x=x


def test():
    run_Iris()

test()