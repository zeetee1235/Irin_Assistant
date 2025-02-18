import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_ollama import OllamaLLM
from langchain.schema import HumanMessage, AIMessage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow ,QWidget
import sys


def record_audio(duration=5, samplerate=44100, filename="voice.wav"): 
    #녹음시작
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    wav.write(filename, samplerate, audio_data)
    #음성파일 저장완료


def transcribe_audio(filename="src/voice.wav"):
    model = whisper.load_model("small").to("cuda") 
    # 모델크기 조절 (tiny, base, small, medium, large)
    # gpu 사용시 NVDA: .to("cuda")  AMD: .to("hip")  MAC: .to("mps")
    # CPU 강제사용 : .to("cpu")
    # 정밀도 연산 끝에 .half() 추가
    result = model.transcribe(filename)
    print("변환된 텍스트:", result["text"])
    return result["text"]



#llm 관련 전역역변수
Irin = OllamaLLM(model="irin")
chat_memory_list = []
chat_memory_CBM= ConversationBufferMemory(llm = Irin) #전체기억 메모리
questsion_number = 0
conversationchain = 0



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
    global conversationchain
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



class MainWindow(QMainWindow): #ui
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(549, 1065)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 60))
        self.widget.setStyleSheet("background-color:#787878\n"
"")


        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(-1, 9, -1, 9)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.side_option_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.side_option_button.sizePolicy().hasHeightForWidth())
        self.side_option_button.setSizePolicy(sizePolicy)
        self.side_option_button.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.side_option_button.setFont(font)
        self.side_option_button.setStyleSheet("border: 0px solid black; \n"
"    background-color: rgba(0, 0, 0, 0); ")
        self.side_option_button.setObjectName("side_option_button")
        self.horizontalLayout.addWidget(self.side_option_button)
        self.top_centor = QtWidgets.QVBoxLayout()
        self.top_centor.setSpacing(0)
        self.top_centor.setObjectName("top_centor")
        self.chat_name = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.chat_name.setFont(font)
        self.chat_name.setObjectName("chat_name")
        self.top_centor.addWidget(self.chat_name)
        self.horizontalLayout.addLayout(self.top_centor)
        self.option_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.option_button.sizePolicy().hasHeightForWidth())
        self.option_button.setSizePolicy(sizePolicy)
        self.option_button.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.option_button.setFont(font)
        self.option_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.option_button.setStyleSheet("border: 0px solid black; \n"
"    background-color: rgba(0, 0, 0, 0); ")
        self.option_button.setObjectName("option_button")
        self.horizontalLayout.addWidget(self.option_button)
        self.horizontalLayout.setStretch(1, 100)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setStyleSheet("background-color:#aaaaaa")
        self.widget_2.setObjectName("widget_2")
        self.display = QtWidgets.QVBoxLayout(self.widget_2)
        self.display.setContentsMargins(9, 0, -1, 9)
        self.display.setSpacing(0)
        self.display.setObjectName("display")
        self.display_top = QtWidgets.QGridLayout()
        self.display_top.setSpacing(0)
        self.display_top.setObjectName("display_top")
        self.scrollArea = QtWidgets.QScrollArea(self.widget_2)
        self.scrollArea.setStyleSheet("background-color:rgba(0,0,0,0)")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 527, 892))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.display_top.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.display.addLayout(self.display_top)
        self.display_bottom = QtWidgets.QGridLayout()
        self.display_bottom.setSpacing(0)
        self.display_bottom.setObjectName("display_bottom")
        self.frame = QtWidgets.QFrame(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 90))
        self.frame.setStyleSheet("background-color: #787878;\n"
"    border-radius: 15px; ")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.chat_grid = QtWidgets.QVBoxLayout(self.frame)
        self.chat_grid.setContentsMargins(5, 0, 5, 0)
        self.chat_grid.setSpacing(0)
        self.chat_grid.setObjectName("chat_grid")
        self.chat_grid_top = QtWidgets.QGridLayout()
        self.chat_grid_top.setContentsMargins(-1, -1, 5, -1)
        self.chat_grid_top.setObjectName("chat_grid_top")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setObjectName("textEdit")
        self.chat_grid_top.addWidget(self.textEdit, 0, 0, 1, 1)
        self.chat_grid.addLayout(self.chat_grid_top)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setStyleSheet("background-color:#000000")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.chat_grid.addWidget(self.line)
        self.chat_grid_bottom = QtWidgets.QGridLayout()
        self.chat_grid_bottom.setContentsMargins(-1, 3, -1, 3)
        self.chat_grid_bottom.setHorizontalSpacing(2)
        self.chat_grid_bottom.setObjectName("chat_grid_bottom")
        self.btn_TTS = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_TTS.sizePolicy().hasHeightForWidth())
        self.btn_TTS.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.btn_TTS.setFont(font)
        self.btn_TTS.setStyleSheet("border: 2px solid black; \n"
"    background-color: rgba(0, 0, 0, 0); \n"
"    border-radius: 10px; \n"
"    padding: 5px; ")
        self.btn_TTS.setObjectName("btn_TTS")
        self.chat_grid_bottom.addWidget(self.btn_TTS, 0, 1, 1, 1)
        self.btn_send = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_send.sizePolicy().hasHeightForWidth())
        self.btn_send.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_send.setFont(font)
        self.btn_send.setStyleSheet("border: 2px solid black; \n"
"    background-color: rgba(0, 0, 0, 0); \n"
"    border-radius: 10px; \n"
"    padding: 5px; ")
        self.btn_send.setObjectName("btn_send")
        self.chat_grid_bottom.addWidget(self.btn_send, 0, 4, 1, 1)
        self.btn_speak = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_speak.sizePolicy().hasHeightForWidth())
        self.btn_speak.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_speak.setFont(font)
        self.btn_speak.setStyleSheet("border: 2px solid black; \n"
"    background-color: rgba(0, 0, 0, 0); \n"
"    border-radius: 10px; \n"
"    padding: 5px; ")
        self.btn_speak.setObjectName("btn_speak")
        self.chat_grid_bottom.addWidget(self.btn_speak, 0, 2, 1, 1)
        self.btn_search = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_search.sizePolicy().hasHeightForWidth())
        self.btn_search.setSizePolicy(sizePolicy)
        self.btn_search.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.btn_search.setFont(font)
        self.btn_search.setStyleSheet("border: 2px solid black; \n"
"    background-color: rgba(0, 0, 0, 0); \n"
"    border-radius: 10px; \n"
"    padding: 5px; ")
        self.btn_search.setObjectName("btn_search")
        self.chat_grid_bottom.addWidget(self.btn_search, 0, 0, 1, 1)
        self.btn_enter = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_enter.sizePolicy().hasHeightForWidth())
        self.btn_enter.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_enter.setFont(font)
        self.btn_enter.setStyleSheet("border: 2px solid black; \n"
"    background-color: rgba(0, 0, 0, 0); \n"
"    border-radius: 10px; \n"
"    padding: 5px; ")
        self.btn_enter.setObjectName("btn_enter")
        self.chat_grid_bottom.addWidget(self.btn_enter, 0, 3, 1, 1)
        self.chat_grid.addLayout(self.chat_grid_bottom)
        self.display_bottom.addWidget(self.frame, 0, 0, 1, 1)
        self.display.addLayout(self.display_bottom)
        self.display.setStretch(0, 100)
        self.display.setStretch(1, 1)
        self.verticalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Irin"))
        self.side_option_button.setText(_translate("MainWindow", ">"))
        self.chat_name.setText(_translate("MainWindow", "HOME"))
        self.option_button.setText(_translate("MainWindow", "\\"))
        self.btn_TTS.setText(_translate("MainWindow", "TTS"))
        self.btn_send.setText(_translate("MainWindow", "send"))
        self.btn_speak.setText(_translate("MainWindow", "speak"))
        self.btn_search.setText(_translate("MainWindow", "search"))
        self.btn_enter.setText(_translate("MainWindow", "Enter"))



class irin_window(MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)



class conversation_irin():

    def __init__(self,chat_memorys,conversationchain):
        self.chat_memorys = chat_memorys
        self.conversationchain = conversationchain #conversationchain 대문자 소문자 주의
        

    def create_questsion_data(self,input,output):
        response_data = {
            "input": input,
            "output": output
        }
        return response_data


    def remove_memory(self):
        if chat_memory_list.count == 100:
            message_to_remove_human = HumanMessage(content = chat_memory_list[0]["input"])
            chat_memory_list.pop(0)
            conversationchain.chat_memory.messages.remove[message_to_remove_human]
        

    def ask_irin(self,user_input):
        answer_data = conversationchain.predict(input=user_input)
        irin_answer = answer_data
        memory_data = create_questsion_data(user_input,answer_data)
        chat_memory_list.append(memory_data)
        remove_memory()
        return irin_answer



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = irin_window()
    window.show()
    sys.exit(app.exec_())

def set_screen():
    x=x

def test():
    set_screen


