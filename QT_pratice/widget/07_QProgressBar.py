import sys
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar
from PySide2.QtCore import QBasicTimer

class MyApp(QWidget):

    def __init__(self):
        super.__init__()
        self.initUI()