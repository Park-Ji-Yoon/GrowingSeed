import sys
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import QIcon

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("My First Application")
        self.setGeometry(500, 100, 500, 500)
        self.show()

        self.setWindowIcon(QIcon('../strawberry.png'))

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 애플리케이션 객체 생성
    ex = MyApp()
    sys.exit(app.exec_())