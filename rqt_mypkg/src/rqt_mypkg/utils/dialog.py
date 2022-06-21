from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
 
class Dialog(QDialog):
  
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Error Dialog")
        message = QLabel("Error! The name of topic is empty.")
       
        QBtn =  QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.layout = QVBoxLayout()   
        self.buttonBox.accepted.connect(self.rejected)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)