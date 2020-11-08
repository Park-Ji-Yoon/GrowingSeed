import sys
from PySide2.QtWidgets import QApplication, QWidget, QPushButton
from PySide2.QtCore import QCoreApplication


class MyApp(QWidget):

  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):
      btn = QPushButton('Quit', self)  # 버튼텍스트, 버튼이 위치할 부모 위젯
      btn.move(50, 50)
      btn.resize(btn.sizeHint())
      # instance()는 현재 인스턴스 반환
      # 여기서 발신자는 푸시버튼 (btn)이고, 수신자는 어플리케이션 객체 (app)
      btn.clicked.connect(QCoreApplication.instance().quit)

      self.setWindowTitle('Quit Button')
      self.setGeometry(300, 300, 300, 200)
      self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
