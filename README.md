"# Irin_assistant" 

to do
.add reset btn
.add tts
.add mic
.add docker
.add voice_detect
.add model size 7B=>3B

done
.stable



필요 메모리 vram

8GB = 7B model

16GB = 13B model

32GB = 33B model


# ollama 설치
curl -fsSL https://ollama.com/install.sh | sh 

# ollama 서비스 시작
systemctl start ollama 

# 모델생성
ollama create irin -f model/Modelfile  

# 모델 확인
ollama list 

# 서버 활성화
node src/server.js 


docker:

cd /home/dev/Irin_Assistant

# 필요한 npm 패키지 설치
npm init -y
npm install express body-parser cors

# Docker 컨테이너 빌드 및 실행
docker compose -f docker/docker-compose.yml up --build

# 도커 실행
docker compose -f docker/docker-compose.yml up