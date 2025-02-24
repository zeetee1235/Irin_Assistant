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


#메모리 가공
def create_questsion_data(input,output):
    global questsion_number
    response_data = {
        "input": input,
        "output": output
    }
    return response_data

#메모리 제거
def remove_memory():
    global chat_memory_list
    if chat_memory_list.count == 100:
        message_to_remove_human = HumanMessage(content = chat_memory_list[0]["input"])
        chat_memory_list.pop(0)
        conversationchain.chat_memory.messages.remove[message_to_remove_human]

#프롬프트 메모리 저장
def save_memory(input_memory_list):
    global chat_memory_CBM
    x = input_memory_list["input"]
    y = input_memory_list["output"]
    chat_memory_CBM.save_context({"input": x}, {"output": y})
    

def clear_all_memory():
    x=x

#대화체인 생성
def generate_conversationchain():
    conversationchain = ConversationChain(
        llm = Irin,
        memory = ConversationBufferMemory()
    ) #conversationchain 대문자 소문자 주의


def run_Irin(): #반복 질문
    global chat_memory_list
    generate_conversationchain()
    while True:
        user_quest = input("질문 입력 (종료: exit): ")
        if user_quest.lower() == "exit":
            break
        answer = conversationchain.predict(input=user_quest)
        memory_data = create_questsion_data(user_quest,answer)
        chat_memory_list.append(memory_data)
        remove_memory()
        print("Iris:", answer)


def ask_Irin(user_quest): #단순질문 앞에 대화체인을 먼저 생성해 놔야함
    global chat_memory_list
    global conversationchain
    answer_data = conversationchain.predict(input=user_quest)
    irin_answer = answer_data
    memory_data = create_questsion_data(user_quest,answer_data)
    chat_memory_list.append(memory_data)
    remove_memory()
    return irin_answer

    
'''