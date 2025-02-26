import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_ollama import OllamaLLM
from langchain.schema import HumanMessage, AIMessage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap, QColor


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
        self.chat_memorys = []
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=Irin,
            memory=self.memory
        )

    def create_questsion_data(self, input, output):  # 메모리 가공
        response_data = {
            "input": input,
            "output": output
        }
        return response_data

    def remove_memory(self):  # 메모리 제거
        if self.chat_memorys.count >= 100:
            """메시지 가져오기"""
            message_to_remove_human = HumanMessage(content=self.chat_memorys[0]["input"])
            message_to_remove_LLM = AIMessage(content=self.chat_memorys[0]["output"])
            """메시지 제거"""
            self.memory.chat_memory.remove[message_to_remove_human]
            self.memory.chat_memory.remove[message_to_remove_LLM]
            self.chat_memorys.pop(0)

    def ask_irin(self, user_input):
        answer_data = self.conversation.predict(input=user_input)
        irin_answer = answer_data
        memory_data = conversation_irin.create_questsion_data(user_input, answer_data)
        self.chat_memorys.append(memory_data)
        return irin_answer



# CustomTextEdit 클래스 정의
class CustomTextEdit(QtWidgets.QTextEdit):
    def __init__(self, placeholder="preview_text", parent=None):
        super().__init__(parent)
        self.placeholder = placeholder
        self.setText(self.placeholder)
        self.has_placeholder = True


    def focusInEvent(self, event):
        if self.has_placeholder:
            self.clear()
            self.has_placeholder = False
        super().focusInEvent(event)


    def focusOutEvent(self, event):
        if not self.toPlainText().strip():
            self.setText(self.placeholder)
            self.has_placeholder = True
        super().focusOutEvent(event)



class MainWindow(QMainWindow):
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

        # 상단 위젯 (헤더 영역)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 60))
        self.widget.setStyleSheet("background-color:#787878;")
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
        self.side_option_button.setStyleSheet("border: 0px solid black; background-color: rgba(0, 0, 0, 0);")
        self.side_option_button.setObjectName("side_option_button")
        self.horizontalLayout.addWidget(self.side_option_button)
        self.top_centor = QtWidgets.QVBoxLayout()
        self.top_centor.setSpacing(0)
        self.top_centor.setObjectName("top_centor")
        self.chat_name = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(15)
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
        self.option_button.setFont(font)
        self.option_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.option_button.setStyleSheet("border: 0px solid black; background-color: rgba(0, 0, 0, 0);")
        self.option_button.setObjectName("option_button")
        self.horizontalLayout.addWidget(self.option_button)
        self.horizontalLayout.setStretch(1, 100)
        self.verticalLayout.addWidget(self.widget)

        # 하단 위젯 (메시지 영역)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setStyleSheet("background-color:#aaaaaa")
        self.widget_2.setObjectName("widget_2")
        self.display = QtWidgets.QVBoxLayout(self.widget_2)
        self.display.setContentsMargins(9, 0, -1, 9)
        self.display.setSpacing(0)
        self.display.setObjectName("display")

        # 상단: 스크롤 영역
        self.display_top = QtWidgets.QGridLayout()
        self.display_top.setSpacing(0)
        self.display_top.setObjectName("display_top")
        self.scrollArea = QtWidgets.QScrollArea(self.widget_2)
        self.scrollArea.setStyleSheet("background-color:rgba(0,0,0,0)")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 527, 892))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollLayout.setSpacing(5)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.display_top.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.display.addLayout(self.display_top)

        # 하단: 입력 영역
        self.display_bottom = QtWidgets.QGridLayout()
        self.display_bottom.setSpacing(0)
        self.display_bottom.setObjectName("display_bottom")

        # 입력창
        self.textEdit = CustomTextEdit("irin:~>", self.widget_2)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("""
            background-color: #787878;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
            color: black;
        """)
        self.display_bottom.addWidget(self.textEdit, 0, 0, 1, 1)
        self.display.addLayout(self.display_bottom)
        self.display.setStretch(0, 100)
        self.display.setStretch(1, 1)
        self.verticalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Irin_Assistant"))
        self.side_option_button.setText(_translate("MainWindow", ">"))
        self.chat_name.setText(_translate("MainWindow", "Irin"))
        self.option_button.setText(_translate("MainWindow", "\\"))


    def setupSignals(self):
        self.textEdit.installEventFilter(self)


    def eventFilter(self, source, event):
        if source == self.textEdit and event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                self.addMessage()
                return True
        return super().eventFilter(source, event)


    def addMessage(self):
        text = self.textEdit.toPlainText().strip()
        if text:
            label = QtWidgets.QLabel(text)
            label.setWordWrap(True)
            label.setStyleSheet("""
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 10px;
                margin: 5px;
                font-size: 14px;
            """)
            label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            # 최대 너비는 scrollArea viewport 너비를 기준으로 설정
            max_width = self.scrollArea.viewport().width() - 20
            label.setMaximumWidth(max_width)
            # QVBoxLayout 사용해서 메시지를 추가 (단, 여기서는 단순하게 addWidget 사용)
            self.scrollLayout.addWidget(label, alignment=QtCore.Qt.AlignRight)
            self.textEdit.clear()
            QtCore.QTimer.singleShot(100, lambda: self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum()))


    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 창 크기 변경 시, 스크롤 영역의 모든 QLabel 최대 너비를 업데이트
        for i in range(self.scrollLayout.count()):
            item = self.scrollLayout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget and isinstance(widget, QtWidgets.QLabel):
                    max_width = self.scrollArea.viewport().width() - 20
                    widget.setMaximumWidth(max_width)
                    widget.adjustSize()



class irin_window(MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setupSignals()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = irin_window()
    window.show()
    sys.exit(app.exec_())