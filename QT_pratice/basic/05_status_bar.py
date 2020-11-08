import sys
from PySide2.QtWidgets import QApplication, QMainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')

        self.setWindowTitle('status bar')
        self.setGeometry(600, 200, 500, 500)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())