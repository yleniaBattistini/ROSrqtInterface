from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from .utils.dialog import Dialog
 
class TopicDialog(QDialog):
    topicText = ""
    
    def __init__(self, topic = ""):
        super().__init__()
        self._topic = ""
        self.setWindowTitle("Topic dialog")
        self.okBtn = QDialogButtonBox.Ok
        cancelBtn = QDialogButtonBox.Cancel
        self.topicText = QTextEdit()
        message = QLabel("Insert the name of the topic!")
       
        QBtn =  self.okBtn| cancelBtn

        self.buttonBox = QDialogButtonBox(QBtn)
        self.layout = QVBoxLayout()   
        self.buttonBox.button(self.okBtn).setEnabled(True)
        self.buttonBox.accepted.connect(self.insertTopic)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(message)
        self.layout.addWidget(self.topicText)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    
    def get_topic(self):
        return self._topic
    
    def set_topic(self, topic):
        self._topic = topic
    
    def insertTopic(self):
        if(self.topicText.toPlainText() == ""):
            Dialog().exec()
        else:
            self.set_topic(self.topicText.toPlainText())
            self.close()
