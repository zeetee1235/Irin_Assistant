import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
import requests

def record_audio(duration=5, samplerate=44100, filename="voice.wav"): # 음성 녹음
    print("녹음 시작")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    wav.write(filename, samplerate, audio_data)
    print("녹음 완료 파일 저장됨:", filename)

def transcribe_audio(filename="voice.wav"): # 음성 텍스트로 변환환
    model = whisper.load_model("small").to("cuda") 
    # 모델크기 조절 (tiny, base, small, medium, large)
    # gpu 사용시 NVDA: .to("cuda")  AMD: .to("hip")  MAC: .to("mps")
    # CPU 강제사용 : .to("cpu")
    #정밀도 연산 끝에 .half() 추가
    result = model.transcribe(filename)
    print("변환된 텍스트:", result["text"])
    return result["text"]

def ask_LLM(question):
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
    
