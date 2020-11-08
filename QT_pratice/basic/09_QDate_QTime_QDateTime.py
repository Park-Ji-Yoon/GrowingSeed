from PySide2.QtCore import QDate, QTime, QDateTime, Qt
from PySide2.QtCore import QDate, Qt
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QDate, Qt

# 현재 날짜
now = QDate.currentDate()
print("현재 날짜 : " + now.toString() + "\n")

# 날짜 형식 지정
now = QDate.currentDate()
print(now.toString('d.M.yy'))
print(now.toString('dd.MM.yyyy'))
print(now.toString('ddd.MMMM.yyyy'))
print(now.toString(Qt.ISODate))  # ISO 표준 형식 yyyy-mm-dd
print(now.toString(Qt.DefaultLocaleLongDate) + "\n") # 어플리케이션 기본 설정

# 현재 시간
time = QTime.currentTime()
print(time.toString() + "\n")

# 시간 형식 지정
time = QTime.currentTime()
print(time.toString('h.m.s'))
print(time.toString('hh.mm.ss'))
print(time.toString('hh.mm.ss.zzz'))
print(time.toString(Qt.DefaultLocaleLongDate))  # 오X h:mm:ss
print(time.toString(Qt.DefaultLocaleShortDate) + "\n")  # 오X h:mm

# 현재 날짜와 시간
datetime = QDateTime.currentDateTime()
print(datetime.toString('d.M.yy hh:mm:ss'))
print(datetime.toString('dd.MM.yyyy, hh:mm:ss'))
print(datetime.toString(Qt.DefaultLocaleLongDate))
print(datetime.toString(Qt.DefaultLocaleShortDate) + "\n")

# 상태 표시줄에 오늘의 날짜를 출력
class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

        self.setWindowTitle('Date')
        self.setGeometry(300, 300, 400, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())