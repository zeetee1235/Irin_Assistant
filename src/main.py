import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_ollama import OllamaLLM
from langchain.schema import HumanMessage, AIMessage
import json
import time

memory_file_path = 'src/memory.json'

def record_audio(duration=5, samplerate=44100, filename="voice.wav"): 
    # 녹음 시작
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    wav.write(filename, samplerate, audio_data)
    # 음성 파일 저장 완료

def transcribe_audio(filename="src/voice.wav"):
    model = whisper.load_model("small").to("cuda") 
    # 모델 크기 조절 (tiny, base, small, medium, large)
    # GPU 사용 시 NVDA: .to("cuda")  AMD: .to("hip")  MAC: .to("mps")
    # CPU 강제 사용 : .to("cpu")
    # 정밀도 연산 끝에 .half() 추가
    result = model.transcribe(filename)
    print("변환된 텍스트:", result["text"])
    return result["text"]

# llm 관련 전역 변수
Irin = OllamaLLM(model="irin")

class conversation_irin():
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=Irin,
            memory=self.memory
        )


    def remove_memory(self):  # 메모리 제거
        if self.chat_memorys.count > 100:
            """메시지 가져오기"""
            message_to_remove_human = HumanMessage(content=self.chat_memorys[0]["input"])
            message_to_remove_LLM = AIMessage(content=self.chat_memorys[0]["output"])
            """메시지 메모리 제거"""
            self.memory.chat_memory.remove[message_to_remove_human]
            self.memory.chat_memory.remove[message_to_remove_LLM]
            """json 파일에서도 제거"""
            with open(memory_file_path, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                if len(data['user_input']) > 100:
                    data['user_input'].pop(0)
                    data['llm_response'].pop(0)
                    file.seek(0)
                    json.dump(data, file, ensure_ascii=False, indent=2)
                    file.truncate()


    def ask_irin(self, user_input):
        answer_data = self.conversation.predict(input=user_input)
        irin_answer = answer_data
        memory_data = self.create_questsion_data(user_input, answer_data)
        self.chat_memorys.append(memory_data)
        return irin_answer

def check_and_respond():
    with open(memory_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if 'user_input' in data and data['user_input']:
        latest_user_message = data['user_input'][-1]
        if len(data['llm_response']) < len(data['user_input']):
            irin = conversation_irin()
            bot_response = irin.ask_irin(latest_user_message)
        

            data['llm_response'].append(bot_response)

            with open(memory_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    while True:
        check_and_respond()
        time.sleep(1)  # 1초마다 확인