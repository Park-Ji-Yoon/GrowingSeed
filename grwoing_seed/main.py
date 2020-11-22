import sys
import threading
import time
from time import sleep

from PySide2 import QtCore, QtGui
from PySide2.QtCore import QTimer, QTime
from PySide2.QtGui import QImage, QFont, QIcon
from PySide2.QtWidgets import *
import pygame

class GrawingSeed(QWidget):

    use_water = 0
    use_pesticide = 0
    use_umbrella = 0

    # 생성자
    def __init__(self):
        super().__init__()
        self.start_growing_seed()

        self.time = 0
        self.which_btn = 0

    # 화면 디자인 요소
    def start_growing_seed(self):
        # 메인 노래 설정
        self.main_music_file = './music/main_music.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.main_music_file)
        pygame.mixer.music.play(-1)
        
        # 메인 화면 설정
        self.main_background_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        main_background = QtGui.QPixmap("./images/main.png")  # 사진 넣을 pixmap
        self.main_background_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.main_background_lb.setPixmap(main_background)  # 메인 배경 사진의 pixmap설정

        # 아이콘 설정
        self.setWindowIcon(QIcon('./images/icon.png'))

        # 게임 기록 버튼
        btn_record = QPushButton("", self.main_background_lb)
        btn_record.setGeometry(90, 475, 180, 85)
        btn_record.clicked.connect(self.btn_record_clicked)
        opacity_effect = QGraphicsOpacityEffect(btn_record)
        opacity_effect.setOpacity(0)
        btn_record.setGraphicsEffect(opacity_effect)

        # 게임 시작 버튼
        btn_start = QPushButton("", self.main_background_lb)
        btn_start.setGeometry(310, 475, 180, 85)
        btn_start.clicked.connect(self.btn_start_clicked)
        opacity_effect = QGraphicsOpacityEffect(btn_start)
        opacity_effect.setOpacity(0)
        btn_start.setGraphicsEffect(opacity_effect)
        
        # 게임 방법 버튼
        btn_rule = QPushButton("", self.main_background_lb)
        btn_rule.setGeometry(530, 475, 180, 85)
        btn_rule.clicked.connect(self.btn_rule_clicked)
        opacity_effect = QGraphicsOpacityEffect(btn_rule)
        opacity_effect.setOpacity(0)
        btn_rule.setGraphicsEffect(opacity_effect)

        # 메인 화면 창
        self.setWindowTitle("Growing Seed")  # 창 제목
        self.resize(800, 650)  # 창 사이즈
        self.center()  # 창을 가운데로 위치
        self.show()  # 창을 보여줌

    # 게임 기록 버튼 이벤트
    def btn_record_clicked(self):
        self.show_game_record()

    # 게임 시작 버튼 이벤트
    def btn_start_clicked(self):
        self.start_play_game()

    # 게임 방법 버튼 이벤트
    def btn_rule_clicked(self):
        self.show_game_rule()

    # 창을 화면은 가운데로 옮겨주는 함수
    def center(self):
        qr = self.frameGeometry()  # 창의 위치와 크기 정보 가져와서 qr에 넣음
        cp = QDesktopWidget().availableGeometry().center()  # 사용하는 모니터 화면의 가운데 위치 파악
        qr.moveCenter(cp)  # 창의 위치를 화면의 중심으로 이동
        self.move(qr.topLeft())  # 현재 창을 qr의 위치로 이동시킴

    def start_play_game(self):
        # 배경 사진 설정
        self.game_background_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        game_background_1 = QtGui.QPixmap("./images/game_1.png")  # 사진 넣을 pixmap
        self.game_background_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.game_background_lb.setPixmap(game_background_1)  # 메인 배경 사진의 pixmap설정

        # 게임 엔진 시작
        self.game_engine()

        self.timer.start()

        self.main_background_lb.setVisible(False)
        self.game_background_lb.setVisible(True)

    def btn_go_home(self):
        self.game_background_lb.setVisible(False)
        self.game_over_lb.setVisible(False)
        self.main_background_lb.setVisible(True)

    # 게임 오버 화면
    def game_over(self):
        # 배경 사진 설정
        self.game_over_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        game_background_3 = QtGui.QPixmap("./images/game_over.png")  # 사진 넣을 pixmap
        self.game_over_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.game_over_lb.setPixmap(game_background_3)  # 메인 배경 사진의 pixmap설정

        self.game_over_home = QPushButton("", self.game_over_lb)
        self.game_over_home.setGeometry(275, 438, 240, 100)
        self.game_over_home.clicked.connect(self.btn_go_home)
        self.game_over_home.setStyleSheet("background-color : yellow;")

    # 게임 엔진
    def game_engine(self):
        self.music_file = './music/background_music_py.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1)

        # 시간 라벨
        self.label_timer = QLabel("0시간", self.game_background_lb)
        self.label_timer.setGeometry(560, 40, 200, 50)
        self.label_timer.setFont(QFont('JalnanOTF', 28))
        self.label_timer.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        
        # 물 준 횟수 라벨
        self.label_water = QLabel("0번", self.game_background_lb)
        self.label_water.setGeometry(610, 200, 150, 40)
        self.label_water.setFont(QFont('JalnanOTF', 18))
        self.label_water.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)

        # 벌레 퇴치 횟수 라벨
        self.label_bug = QLabel("0번", self.game_background_lb)
        self.label_bug.setGeometry(610, 250, 150, 50)
        self.label_bug.setFont(QFont('JalnanOTF', 18))
        self.label_bug.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)

        # 환경오염 막은 횟수 라벨
        self.label_clean = QLabel("0번", self.game_background_lb)
        self.label_clean.setGeometry(610, 300, 150, 50)
        self.label_clean.setFont(QFont('JalnanOTF', 18))
        self.label_clean.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)

        # 시간
        self.timer = QTimer(self.game_background_lb)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeout)

        # 캐릭터 버튼
        self.btn_char = QPushButton("", self.game_background_lb)
        self.btn_char.setGeometry(249, 100, 297.5, 305)
        self.btn_char.clicked.connect(self.btn_char_clicked)
        self.btn_char.setStyleSheet("background-image : url(./images/first_stage.png); border: 0px solid black;")

        # 물주기 버튼
        self.btn_water = QPushButton("", self.game_background_lb)
        self.btn_water.setGeometry(220, 495, 100, 100)
        self.btn_water.clicked.connect(self.btn_water_clicked)
        self.btn_water.setStyleSheet("background-image : url(./images/watering.png); border: 0px solid black;")

        # 살충제 버튼
        self.btn_pesticide = QPushButton("", self.game_background_lb)
        self.btn_pesticide.setGeometry(350, 495, 100, 100)
        self.btn_pesticide.clicked.connect(self.btn_pesticide_clicked)
        self.btn_pesticide.setStyleSheet("background-image : url(./images/pesticide.png); border: 0px solid black;")

        # 우산 버튼
        self.btn_umbrella = QPushButton("", self.game_background_lb)
        self.btn_umbrella.setGeometry(480, 495, 100, 100)
        self.btn_umbrella.clicked.connect(self.btn_umbrella_clicked)
        self.btn_umbrella.setStyleSheet("background-image : url(./images/umbrella.png); border: 0px solid black;")

        btn_gotohome = QPushButton("", self.game_background_lb)
        btn_gotohome.setGeometry(52, 50, 50, 50)
        btn_gotohome.clicked.connect(self.gotohome)
        opacity_effect = QGraphicsOpacityEffect(btn_gotohome)
        opacity_effect.setOpacity(0)
        btn_gotohome.setGraphicsEffect(opacity_effect)

    # 게임 오버되었는지 확인하는 함수
    def game_over_check(self):
        # 한 아이템당 사용 횟수가 10 이상이면 게임 오버
        if GrawingSeed.use_water >= 10 or GrawingSeed.use_pesticide >= 10 or GrawingSeed.use_umbrella >= 10:
            self.item_timer.stop()  # 타이머를 멈춤
            GrawingSeed.water_btn_time = 0  # 아이템 초수 초기화
            GrawingSeed.pesticide_btn_time = 0  # 아이템 초수 초기화
            GrawingSeed.umbrella_btn_time = 0  # 아이템 초수 초기화
            self.game_background_lb.setVisible(False)
            self.game_over_lb.setVisible(True)

    # 게임 중단 확인 dialog
    def gotohome(self):
        reply = QMessageBox.question(self, '게임 중단', '정말 게임을 중단하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.game_background_lb.setVisible(False)
            self.main_background_lb.setVisible(True)
            self.main_music_file = './music/main_music.mp3'
            
            # 게임을 중단하고 메인으로 돌아갔을 때 메인화면 음악 재생
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(self.main_music_file)
            pygame.mixer.music.play(-1)
        else:
            pass

    def timeout(self):
        sender = self.sender()
        self.time += 1
        if id(sender) == id(self.timer):
            if self.time % 10 == 0:
                self.label_timer.setText(str(self.time // 10) + "시간")

    btn_timer_flag = 4
    water_btn_time = 0
    pesticide_btn_time = 0
    umbrella_btn_time = 0

    def printTime(self):
        if self.btn_timer_flag == 0:
            GrawingSeed.water_btn_time += 1
            print(f'물뿌리개 타이머 : {GrawingSeed.water_btn_time}')
        elif self.btn_timer_flag == 1:
            GrawingSeed.pesticide_btn_time += 1
            print(f'살충제 타이머 : {GrawingSeed.pesticide_btn_time}')
        elif self.btn_timer_flag == 2:
            GrawingSeed.umbrella_btn_time += 1
            print(f'우산 타이머 : {GrawingSeed.umbrella_btn_time}')

        if GrawingSeed.water_btn_time == 5 or GrawingSeed.pesticide_btn_time == 5 or GrawingSeed.umbrella_btn_time == 5:
            GrawingSeed.water_btn_time = 0
            GrawingSeed.pesticide_btn_time = 0
            GrawingSeed.umbrella_btn_time = 0
            self.btn_timer_flag = 4
            self.btn_water.setEnabled(True)  # 물뿌리개 버튼 활성화
            self.btn_pesticide.setEnabled(True)
            self.btn_umbrella.setEnabled(True)
            self.item_timer.stop()
            self.btn_water.setStyleSheet("background-image : url(./images/watering.png); border: 0px solid black;")
            self.btn_pesticide.setStyleSheet("background-image : url(./images/pesticide.png); border: 0px solid black;")
            self.btn_umbrella.setStyleSheet("background-image : url(./images/umbrella.png); border: 0px solid black;")
            self.btn_char.setStyleSheet("background-image : url(./images/first_stage.png); border: 0px solid black;")

        self.game_over()
        self.game_over_check()

    def btn_char_clicked(self):
        # 버튼 눌렸을 때 각각 시간을 재는 타이머들 초기화
        
        # 물뿌리개 타이머
        self.item_timer = QTimer(self.game_background_lb)
        self.item_timer.setInterval(1000)
        self.item_timer.timeout.connect(self.printTime)

        if self.which_btn == 1:
            GrawingSeed.use_water += 1
            self.label_water.setText(str(GrawingSeed.use_water) + "번")

            try:
                self.btn_timer_flag = 0
                self.item_timer.start()    # 물뿌리개 타이머 시작
                self.btn_water.setEnabled(False)    # 물뿌리개 버튼 비활성화
                self.btn_pesticide.setEnabled(False)
                self.btn_umbrella.setEnabled(False)
                print("물뿌리개다!!")    # 디버깅용
                self.which_btn = 0
                self.setCursor(QtCore.Qt.PointingHandCursor)    # 커서 설정
                self.btn_water.setStyleSheet("background-image : url(./images/watering_false.png); border: 0px solid black;")
                self.btn_pesticide.setStyleSheet("background-image : url(./images/pesticide_false.png); border: 0px solid black;")
                self.btn_umbrella.setStyleSheet("background-image : url(./images/umbrella_false.png); border: 0px solid black;")
                self.btn_char.setStyleSheet("background-image : url(./images/first_stage_water.png); border: 0px solid black;")
                
            except:
                print("물뿌리개 에러---")

        elif self.which_btn == 2:
            GrawingSeed.use_pesticide += 1
            self.label_bug.setText(str(GrawingSeed.use_pesticide) + "번")

            try:
                self.btn_timer_flag = 1
                self.item_timer.start()
                self.btn_water.setEnabled(False)  # 물뿌리개 버튼 비활성화
                self.btn_pesticide.setEnabled(False)
                self.btn_umbrella.setEnabled(False)
                print("살충제다!!")
                self.which_btn = 0
                self.setCursor(QtCore.Qt.PointingHandCursor)
                self.btn_water.setStyleSheet("background-image : url(./images/watering_false.png); border: 0px solid black;")
                self.btn_pesticide.setStyleSheet("background-image : url(./images/pesticide_false.png); border: 0px solid black;")
                self.btn_umbrella.setStyleSheet("background-image : url(./images/umbrella_false.png); border: 0px solid black;")
                self.btn_char.setStyleSheet("background-image : url(./images/first_stage_pesticide.png); border: 0px solid black;")
                
            except:
                print("살충제 에러---")
                
        elif self.which_btn == 3:
            GrawingSeed.use_umbrella += 1
            self.label_clean.setText(str(GrawingSeed.use_umbrella) + "번")

            try:
                self.btn_timer_flag = 2
                self.item_timer.start()
                self.btn_water.setEnabled(False)  # 물뿌리개 버튼 비활성화
                self.btn_pesticide.setEnabled(False)
                self.btn_umbrella.setEnabled(False)
                print("우산이다!!")
                self.which_btn = 0
                self.setCursor(QtCore.Qt.PointingHandCursor)
                self.btn_water.setStyleSheet("background-image : url(./images/watering_false.png); border: 0px solid black;")
                self.btn_pesticide.setStyleSheet("background-image : url(./images/pesticide_false.png); border: 0px solid black;")
                self.btn_umbrella.setStyleSheet("background-image : url(./images/umbrella_false.png); border: 0px solid black;")
                self.btn_char.setStyleSheet("background-image : url(./images/first_stage_umbrella.png); border: 0px solid black;")

            except:
                print("우산 에러---")
                
        else:
            self.none_item()

    # 물 아이템 클릭
    def btn_water_clicked(self):
        cursor_water = QtGui.QCursor(QtGui.QPixmap('./images/watering_cursor.png'))
        self.setCursor(cursor_water)
        self.which_btn = 1

    # 살충제 아이템 클릭
    def btn_pesticide_clicked(self):
        cursor_pesticide = QtGui.QCursor(QtGui.QPixmap('./images/pesticide_cursor.png'))
        self.setCursor(cursor_pesticide)
        self.which_btn = 2

    # 우산 아이템 클릭
    def btn_umbrella_clicked(self):
        cursor_umbrella = QtGui.QCursor(QtGui.QPixmap('./images/umbrella_cursor.png'))
        self.setCursor(cursor_umbrella)
        self.which_btn = 3

    # 게임 방법
    def show_game_rule(self):
        self.rule_background_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        rule_background = QtGui.QPixmap("./images/rule.png")  # 사진 넣을 pixmap
        self.rule_background_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.rule_background_lb.setPixmap(rule_background)  # 메인 배경 사진의 pixmap설정

        # 뒤로가기 버튼
        btn_return = QPushButton("", self.rule_background_lb)
        btn_return.setGeometry(75, 55, 60, 60)
        btn_return.clicked.connect(self.btn_return_clicked)
        opacity_effect = QGraphicsOpacityEffect(btn_return)
        opacity_effect.setOpacity(0)
        btn_return.setGraphicsEffect(opacity_effect)

        self.main_background_lb.setVisible(False)
        self.rule_background_lb.setVisible(True)

    # 게임 기록 
    def show_game_record(self):
        pass

    def btn_enabled(self):
        global count
        count += 1
        print(count)
        timer = threading.Timer(10, self.btn_enabled())
        timer.start()

        if count == 5:
            print("버튼 사용 가능")
            timer.cancel()
            return True


    # 뒤로가기 버튼
    def btn_return_clicked(self):
        self.main_background_lb.setVisible(True)
        self.rule_background_lb.setVisible(False)

    def none_item(self):
        reply = QMessageBox.question(self, '아이템 없음', '아이템을 선택해주세요', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            return
        else:
            self.game_background_lb.setVisible(False)
            self.main_background_lb.setVisible(True)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '게임 종료', '정말 게임을 종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# 실행하는 메인함수
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 애플리케이션 객체 생성
    ex = GrawingSeed()
    sys.exit(app.exec_())