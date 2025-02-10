#잡다한거 테스트용


from langchain.memory import ConversationBufferMemory

# 기존 메모리 초기화
memory = ConversationBufferMemory()

# 대화 저장
memory.save_context({"input": "안녕하세요!"}, {"output": "안녕하세요! 무엇을 도와드릴까요?"})

# 메모리 재설정
memory = ConversationBufferMemory()  # 새로운 메모리 객체로 교체
