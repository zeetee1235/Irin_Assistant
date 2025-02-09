from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain_community.llms import Ollama

# LLM 초기화
llm = Ollama(model="Iris")

# 요약 메모리 초기화
memory = ConversationSummaryMemory(llm=llm)

# 대화 체인 생성
conversation = ConversationChain(
    llm=llm,
    memory=memory,
)

# 대화
response = conversation.predict(input = "제 2차 세계대전에서 나치독일과 소련사이에 발발한 독소전쟁에 대해 설명해줘")
print(response)

response = conversation.predict(input = "독소전쟁이 뭐였지?")
print(response)
