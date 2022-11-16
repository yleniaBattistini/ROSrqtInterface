from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from .utils.dialog import Dialog
 
class TopicDialog(QDialog):
    topicTextPub = ""
    topicTextSub = ""
    
    def __init__(self, topic = ""):
        super().__init__()
        self._topic = ""
        self.setWindowTitle("Topic input dialog")
        self.okBtn = QDialogButtonBox.Ok
        cancelBtn = QDialogButtonBox.Cancel
        self.topicTextPub = QTextEdit()
        messagePub = QLabel("Insert the name of topic - PUBLISHER!")
        self.topicTextSub = QTextEdit()
        messageSub = QLabel("Insert the name of topic - SUBSCRIBER!")
       
        QBtn =  self.okBtn| cancelBtn

        self.buttonBox = QDialogButtonBox(QBtn)
        self.layout = QVBoxLayout()   
        self.buttonBox.button(self.okBtn).setEnabled(True)
        self.buttonBox.accepted.connect(self.insertTopic)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(messagePub)
        self.layout.addWidget(self.topicTextPub)
        self.layout.addWidget(messageSub)
        self.layout.addWidget(self.topicTextSub)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    
    def get_topicInput(self):
        return self.topicTextPub

    def get_topicOutput(self):
        return self.topicTextSub
    
    def set_topic(self, topicPub, topicSub):
        self.topicTextPub = topicPub
        self.topicTextSub = topicSub
    
    def insertTopic(self):
        if((len(self.topicTextPub.toPlainText()) == 0)  or (len(self.topicTextSub.toPlainText()) == 0)) :
            Dialog().exec()
        else:
            self.set_topic(self.topicTextPub.toPlainText(), self.topicTextSub.toPlainText())
            self.close()
