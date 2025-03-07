import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import OllamaLLM  # Changed from Ollama to OllamaLLM
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import json
import time
import os

memory_file_path = 'src/memory.json'

def record_audio(duration=5, samplerate=44100, filename="voice.wav"): 
    # 녹음 시작
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    wav.write(filename, samplerate, audio_data)
    # 음성 파일 저장 완료

def transcribe_audio(filename="src/voice.wav"):
    model = whisper.load_model("small").to("cpu") 
    # 모델 크기 조절 (tiny, base, small, medium, large)
    # GPU 사용 시 NVDA: .to("cuda")  AMD: .to("hip")  MAC: .to("mps")
    # CPU 강제 사용 : .to("cpu")
    # 정밀도 연산 끝에 .half() 추가
    result = model.transcribe(filename)
    print("변환된 텍스트:", result["text"])
    return result["text"]

class conversation_irin():
    def __init__(self):
        self.chat_history = ChatMessageHistory()
        self.chat_memorys = []
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "당신은 유용한 AI 어시스턴트 이린입니다. 사용자의 질의에 대해 친근하고 정확하게 한국어로 답변해야 합니다."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # Create chain with message history
        self.conversation = RunnableWithMessageHistory(
            prompt | OllamaLLM(model="irin", base_url="http://ollama:11434"),  # Changed from Ollama to OllamaLLM
            lambda session_id: self.chat_history,
            input_messages_key="input",
            history_messages_key="history"
        )

    def create_questsion_data(self, user_input, answer_data):
        """Create a dictionary containing the conversation data."""
        return {
            "input": user_input,
            "output": answer_data,
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

    def ask_irin(self, user_input):
        """Send a message to Irin and get response."""
        try:
            response = self.conversation.invoke({"input": user_input})
            answer = response.content if hasattr(response, 'content') else str(response)
            
            # Store the conversation in memory
            memory_data = self.create_questsion_data(user_input, answer)
            self.chat_memorys.append(memory_data)
            
            # Add messages to chat history
            self.chat_history.add_user_message(user_input)
            self.chat_history.add_ai_message(answer)
            
            return answer
            
        except Exception as e:
            print(f"Error in ask_irin: {e}")
            return f"죄송합니다. 오류가 발생했습니다: {str(e)}"

    def remove_memory(self):  # 메모리 제거
        if self.chat_memorys.count > 100:
            """메시지 가져오기"""
            message_to_remove_human = HumanMessage(content=self.chat_memorys[0]["input"])
            message_to_remove_LLM = AIMessage(content=self.chat_memorys[0]["output"])
            """메시지 메모리 제거"""
            self.chat_history.remove[message_to_remove_human]
            self.chat_history.remove[message_to_remove_LLM]
            """json 파일에서도 제거"""
            with open(memory_file_path, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                if len(data['user_input']) > 100:
                    data['user_input'].pop(0)
                    data['llm_response'].pop(0)
                    file.seek(0)
                    json.dump(data, file, ensure_ascii=False, indent=2)
                    file.truncate()

def check_and_respond():
    """Check for new messages and respond."""
    try:
        with open(memory_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if 'user_input' in data and data['user_input']:
            latest_user_message = data['user_input'][-1]
            if len(data['llm_response']) < len(data['user_input']):
                irin = conversation_irin()
                bot_response = irin.ask_irin(latest_user_message)
                print(f"User: {latest_user_message}")
                print(f"Irin: {bot_response}")

                data['llm_response'].append(bot_response)

                with open(memory_file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error in check_and_respond: {e}")

if __name__ == "__main__":
    while True:
        check_and_respond()
        time.sleep(1)  # 1초마다 확인