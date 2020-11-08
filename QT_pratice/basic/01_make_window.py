import sys
from PySide2.QtWidgets import QApplication, QWidget

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("My First Application")
        self.move(300, 300)
        self.resize(400, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 애플리케이션 객체 생성
    ex = MyApp()
    sys.exit(app.exec_())