# import csv
#
# import pandas as pd
#
# f = open('./text/write.csv', 'a', newline='', encoding="utf-8")
# wr = csv.writer(f)
# wr.writerow([1, '림코딩', '부산'])
# wr.writerow([2, '김갑환', '서울'])
#
# f.close()

# from datetime import datetime
# today = datetime.today()
# year = today.year
# month = today.month
# day = today.day
# hour = today.hour
# minute = today.minute
# current_time = str(year)[-2:] + str(month) + str(day) + str(hour) + str(minute)
# print(current_time)

# import sys
# from PySide2 import QtGui, QtCore, QtWidgets
# from PySide2.QtMultimedia import QSound
# from PySide2.QtWidgets import QApplication, QPushButton
#
#
# class Example(QtWidgets.QMainWindow):
#        def __init__(self):
#            QtWidgets.QMainWindow.__init__(self)
#            self.initUI()
#        def initUI(self):
#            self.setGeometry(300,300,200,200)
#            self.b1 = QPushButton("Play", self)
#            self.b1.clicked.connect(self.Play)
#            self.b1.move(50, 80)
#
#        def Play(self):
#            QSound.play("./music/background_music_py.mp3")
#
# def main():
#        app = QApplication(sys.argv)
#        ex = Example()
#        ex.show()
#        sys.exit(app.exec_())
# if __name__ == "__main__":
#        main()

# import winsound
#
# def main():
#     so1 = {'do':261, 're':293, 'mi':329, 'pa':349, 'sol':391, 'ra':440, 'si':493}
#     mel = ['do', 'mi', 'mi', 'mi', 'sol', 're', 'pa', 'pa', 'ra', 'si', 'si']
#     dur = [4, 4, 2, 4, 4, 2, 4, 4, 2, 4, 4, 2]
#     mel2 = ['sol', 'do', 'ra', 'pa', 'mi', 'do', 're']
#     dur2 = [1, 1, 1, 1, 1, 1, 1]
#
#     music = zip(mel, dur)
#     muaic2 = zip(mel2, dur2)
#
#     for melody, duration in music:
#         winsound.Beep(so1[melody], 1000)
#
#     for melody, duration in muaic2:
#         winsound.Beep(so1[melody], 1000)
#
# if __name__ == '__main__':
#     main()

# from PySide2.QtMultimedia import QSound
# bells = QSound("./music/background_music_py.mp3")
# bells.play()
# bells.loops()
from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QSoundEffect
effect = QSoundEffect
url = QUrl()
url.fromLocalFile("./music/background_music_py.mp3")
effect.setSource(url.fromLocalFile("./music/background_music_py.mp3"))
effect.setLoopCount(100)
effect.setVolume(0.25)
effect.play()