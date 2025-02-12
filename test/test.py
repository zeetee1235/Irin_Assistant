#잡다한거 테스트용

'''
from langchain.memory import ConversationBufferMemory

chat_memory = []

chat_memory.append = ConversationBufferMemory()

chat_memory.append = ConversationBufferMemory()

chat_memory.append = ConversationBufferMemory()


print(chat_memory.count)

# 기존 메모리 초기화
memory = ConversationBufferMemory()

# 대화 저장
memory.save_context({"input": "안녕하세요!"}, {"output": "안녕하세요! 무엇을 도와드릴까요?"})

# 메모리 재설정
memory = ConversationBufferMemory()  # 새로운 메모리 객체로 교체

memory.clear()
'''

from langchain.memory import ConversationBufferMemory

# 메모리 객체 초기화
memory = ConversationBufferMemory()

# memory에 대화 내용 저장
memory.save_context({"input": "안녕"}, {"output": "안녕하세요! 무엇을 도와드릴까요?"})
memory.save_context({"input": "오늘 날씨 어때?"}, {"output": "오늘은 맑은 날씨입니다."})

# 현재 메모리 내용 확인
print("Before removal:", memory.load_memory_variables({}))

# 특정 메시지 제거 (예: 첫 번째 메시지)
if len(memory.chat_memory.messages) > 0:
    del memory.chat_memory.messages[0]

# 메시지 제거 후 메모리 내용 확인
print("After removal:", memory.load_memory_variables({}))


chat_memory_list = []
chat_memory_CBM_list = []
chat_memory_CSM_list = []


def organize_memory():
    global chat_memory_list
    global chat_memory_CBM_list
    global chat_memory_CSM_list
    if chat_memory_list.count == 250:
        chat_memory_list.pop(0)
    if chat_memory_CBM_list.count == 50:
        chat_memory_CBM_list.pop(0)
    if chat_memory_CSM_list.count == 150:
        chat_memory_CSM_list.pop(0)

