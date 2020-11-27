import sys
import threading
import random

from PySide2 import QtCore, QtGui
from PySide2.QtCore import QTimer, Qt
from PySide2.QtGui import QFont, QIcon, QPixmap
from PySide2.QtWidgets import *
import pygame

class GrawingSeed(QWidget):
    use_water = 0
    use_pesticide = 0
    use_umbrella = 0

    current_level = 0

    # 생성자
    def __init__(self):
        super().__init__()
        self.start_growing_seed()

        self.time = 0
        self.bug_time = 0
        self.dust_time = 0
        self.which_btn = 0

        self.isBug = False
        self.isDust = False

        self.bug_success = 0
        self.dust_success = 0

        self.change_dust = True

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
        opacity_effect = QGraphicsOpacityEffect(self.game_over_home)
        opacity_effect.setOpacity(0)
        self.game_over_home.setGraphicsEffect(opacity_effect)
        self.game_over_home.setStyleSheet("background-color: red")

        # 아이템 사용 횟수 0으로 초기화
        self.use_water = 0
        self.use_pesticide = 0
        self.use_umbrella = 0

        self.dust_times = []
        self.dust_count = 0

        # self.timer.stop()
        # self.time = 0

    # 씨앗씨 키우기 성공 화면
    def game_success(self):
        # 점수 계산 함수 호출
        score_result = self.mark_score()
        
        # 보너스 점수 초기화
        bonus = 0

        # 별 갯수 초기화
        self.star_count = 0

        self.game_success_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨

        # 점수 라벨
        self.score_label = QLabel("0점", self.game_success_lb)
        self.score_label.setGeometry(100, 180, 700, 300)
        self.score_label.setFont(QFont('JalnanOTF', 60))
        self.score_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)

        # 배경 사진 설정
        if score_result <= 200:
            game_background_4 = QtGui.QPixmap("./images/one_star.png")  # 사진 넣을 pixmap
            self.game_success_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
            self.game_success_lb.setPixmap(game_background_4)  # 메인 배경 사진의 pixmap설정
            bonus = 20
            self.star_count = 1
            self.score_label.setText(str(score_result + bonus) + "점")
        elif score_result <= 400:
            game_background_4 = QtGui.QPixmap("./images/two_stars.png.png")  # 사진 넣을 pixmap
            self.game_success_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
            self.game_success_lb.setPixmap(game_background_4)  # 메인 배경 사진의 pixmap설정
            bonus = 50
            self.star_count = 2
            self.score_label.setText(str(score_result + bonus) + "점")
        elif score_result <= 600:
            game_background_4 = QtGui.QPixmap("./images/three_stars.png")  # 사진 넣을 pixmap
            self.game_success_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
            self.game_success_lb.setPixmap(game_background_4)  # 메인 배경 사진의 pixmap설정
            bonus = 90
            self.star_count = 3
            self.score_label.setText(str(score_result + bonus) + "점")
        elif score_result <= 800:
            game_background_4 = QtGui.QPixmap("./images/four_stars.png")  # 사진 넣을 pixmap
            self.game_success_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
            self.game_success_lb.setPixmap(game_background_4)  # 메인 배경 사진의 pixmap설정
            bonus = 140
            self.star_count = 4
            self.score_label.setText(str(score_result + bonus) + "점")
        elif score_result <= 1000:
            game_background_4 = QtGui.QPixmap("./images/five_stars.png")  # 사진 넣을 pixmap
            self.game_success_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
            self.game_success_lb.setPixmap(game_background_4)  # 메인 배경 사진의 pixmap설정
            bonus = 200
            self.star_count = 5
            self.score_label.setText(str(score_result + bonus) + "점")
        else:
            print("에러 : 나올 수 없는 점수 나옴")

        # 물 준 횟수, 살충제 사용 횟수, 우산 사용 횟수 0으로 초기화
        # 아이템 사용 횟수 0으로 초기화
        self.use_water = 0
        self.use_pesticide = 0
        self.use_umbrella = 0

        self.btn_go_main = QPushButton("", self.game_success_lb)
        self.btn_go_main.setGeometry(132, 517, 240, 80)
        self.btn_go_main.clicked.connect(self.go_to_home)
        opacity_effect1 = QGraphicsOpacityEffect(self.btn_go_main)
        opacity_effect1.setOpacity(0)
        self.btn_go_main.setGraphicsEffect(opacity_effect1)

        self.record_btn = QPushButton("", self.game_success_lb)
        self.record_btn.setGeometry(430, 517, 240, 80)
        self.record_btn.clicked.connect(self.write_game_record)
        opacity_effect2 = QGraphicsOpacityEffect(self.record_btn)
        opacity_effect2.setOpacity(0)
        self.record_btn.setGraphicsEffect(opacity_effect2)

        self.main_background_lb.setVisible(False)
        self.game_over_lb.setVisible(False)
        self.game_success_lb.setVisible(True)

        # 게임 종료시 모든 타이머 종료
        self.timer.stop()
        self.dust_timer.stop()
        self.bug_timer.stop()
        self.item_timer.stop()

    # 점수를 계산하는 함수
    def mark_score(self):
        self.score = self.use_water * 8 +  self.bug_success * 13 + self.dust_success * 13 + (120 - self.time) * 10
        print(f'**점수** : " + {self.score}')
        return self.score
    
    # 게임 엔진
    def game_engine(self):
        self.music_file = './music/background_music_py.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1)

        GrawingSeed.current_level = 1

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

        self.game_over()

        # 환경 오염 발생 준비
        self.dust_times = []  # 환경 오염이 발생할 시간 담을 list
        self.dust_count = random.randint(2, 5)  # 환경 오염 발생 횟수
        rand_num = random.randrange(1, 50, 7)
        # 겹치지 않게 self.dust_count만큼 랜덤 숫자를 뽑음
        for i in range(self.dust_count):
            while rand_num in self.dust_times:
                rand_num = random.randrange(1, 50, 7)
            self.dust_times.append(rand_num)
        print("정렬 전 : " + str(self.dust_times))  # 디버깅용
        self.dust_times.sort()
        print("정렬 후 : " + str(self.dust_times))  # 디버깅용

    # 게임 오버되었는지 확인하는 함수
    def game_over_check(self):
        # 한 아이템당 사용 횟수가 10 이상이면 게임 오버
        if GrawingSeed.use_water >= 10 or GrawingSeed.use_pesticide >= 10 or GrawingSeed.use_umbrella >= 10:
            # self.item_timer.stop()  # 타이머를 멈춤
            GrawingSeed.water_btn_time = 0  # 아이템 초수 초기화
            GrawingSeed.pesticide_btn_time = 0  # 아이템 초수 초기화
            GrawingSeed.umbrella_btn_time = 0  # 아이템 초수 초기화
            self.game_background_lb.setVisible(False)
            self.game_over_lb.setVisible(True)

    def growing(self, level):
        if level == 1:
            if GrawingSeed.use_water >= 2 and self.bug_success >= 1 and self.dust_success >= 0:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/second_stage.png); border: 0px solid black;")
                GrawingSeed.current_level = 2

        elif level == 2:
            if GrawingSeed.use_water >= 4 and self.bug_success >= 2 and self.dust_success >= 0:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/third_stage.png); border: 0px solid black;")
                GrawingSeed.current_level = 3

        elif level == 3:
            if GrawingSeed.use_water >= 6 and self.bug_success >= 3 and self.dust_success >= 0:
                self.btn_char.setStyleSheet("background-image : url(./images/last_stage.png); border: 0px solid black;")
                GrawingSeed.current_level = 4

        elif level == 4:
            if GrawingSeed.use_water >= 8 and self.bug_success >= 4 and self.dust_success >= 1:
                self.game_success()

                GrawingSeed.water_btn_time = 0  # 아이템 초수 초기화
                GrawingSeed.pesticide_btn_time = 0  # 아이템 초수 초기화
                GrawingSeed.umbrella_btn_time = 0  # 아이템 초수 초기화

    # 게임 중단 확인 dialog
    def gotohome(self):
        reply = QMessageBox.question(self, '게임 중단', '정말 게임을 중단하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.game_background_lb.setVisible(False)
            self.main_background_lb.setVisible(True)
            self.main_music_file = './music/main_music.mp3'

            self.timer.stop()
            self.time = 0

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
            # 7로 나누어 떨어질 때바다 벌레가 출몰
            if self.time % 15 == 0:
                self.bug(GrawingSeed.current_level)
            # 게임 시작 시 설정한 시간마다 환경오염 발생
            for i in self.dust_times:
                if i == self.time:
                    self.dust(GrawingSeed.current_level)

    btn_timer_flag = 4
    water_btn_time = 0
    pesticide_btn_time = 0
    umbrella_btn_time = 0

    def bug(self, level):
        self.bug_timer = QTimer(self.game_background_lb)
        self.bug_timer.setInterval(1000)
        self.bug_timer.timeout.connect(self.bugtimeout)
        self.bug_timer.start()
        self.isBug = True

        if level == 1:
            self.btn_char.setStyleSheet(
                "background-image : url(./images/first_stage_bug.png); border: 0px solid black;")
        elif level == 2:
            self.btn_char.setStyleSheet(
                "background-image : url(./images/second_stage_bug.png); border: 0px solid black;")
        elif level == 3:
            self.btn_char.setStyleSheet(
                "background-image : url(./images/third_stage_bug.png); border: 0px solid black;")
        elif level == 4:
            self.btn_char.setStyleSheet("background-image : url(./images/last_stage_bug.png); border: 0px solid black;")

    def bugtimeout(self):
        sender = self.sender()
        self.bug_time += 1
        if id(sender) == id(self.bug_timer):
            print("벌레 출몰한 지 : " + str(self.bug_time) + "초")
        if self.bug_time >= 10:
            print("벌레에게 죽음-----")
            self.bug_timer.stop()
            self.bug_time = 0
            self.game_over_check()
            self.game_background_lb.setVisible(False)
            self.game_over_lb.setVisible(True)

    def dust(self, level):
        self.dust_timer = QTimer(self.game_background_lb)
        self.dust_timer.setInterval(1000)
        self.dust_timer.timeout.connect(self.dusttimeout)
        self.dust_timer.start()
        self.isDust = True

        if level == 1:
            if self.change_dust == True:
                self.btn_char.setStyleSheet("background-image : url(./images/first_stage_dust.png); border: 0px solid black;")
                self.change_dust = False
            else:
                self.btn_char.setStyleSheet("background-image : url(./images/first_stage_acid.png); border: 0px solid black;")
                self.change_dust = True
        elif level == 2:
            if self.change_dust == True:
                self.btn_char.setStyleSheet("background-image : url(./images/second_stage_dust.png); border: 0px solid black;")
                self.change_dust = False
            else:
                self.btn_char.setStyleSheet("background-image : url(./images/second_stage_acid.png); border: 0px solid black;")
                self.change_dust = True
        elif level == 3:
            if self.change_dust == True:
                self.btn_char.setStyleSheet("background-image : url(./images/third_stage_dust.png); border: 0px solid black;")
                self.change_dust = False
            else:
                self.btn_char.setStyleSheet("background-image : url(./images/third_stage_acid.png); border: 0px solid black;")
                self.change_dust = True
        elif level == 4:
            if self.change_dust == True:
                self.btn_char.setStyleSheet("background-image : url(./images/last_stage_dust.png); border: 0px solid black;")
                self.change_dust = False
            else:
                self.btn_char.setStyleSheet("background-image : url(./images/last_stage_acid.png); border: 0px solid black;")
                self.change_dust = True

    def dusttimeout(self):
        sender = self.sender()
        self.dust_time += 1
        if id(sender) == id(self.dust_timer):
            print("환경오염 발생한 지 : " + str(self.dust_time) + "초")
        if self.dust_time >= 10:
            print("환경오염으로 죽음-----")
            self.dust_timer.stop()
            self.dust_time = 0
            self.game_over_check()
            self.game_background_lb.setVisible(False)
            self.game_over_lb.setVisible(True)

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
            self.dust_timer.stop()

        if GrawingSeed.water_btn_time == 2 or GrawingSeed.pesticide_btn_time == 2 or GrawingSeed.umbrella_btn_time == 2:
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

            if GrawingSeed.current_level == 1:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/first_stage.png); border: 0px solid black;")
            elif GrawingSeed.current_level == 2:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/second_stage.png); border: 0px solid black;")
            elif GrawingSeed.current_level == 3:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/third_stage.png); border: 0px solid black;")
            elif GrawingSeed.current_level == 4:
                self.btn_char.setStyleSheet("background-image : url(./images/last_stage.png); border: 0px solid black;")

        self.game_over_check()
        self.growing(GrawingSeed.current_level)

    def btn_char_clicked(self):
        # 버튼 눌렸을 때 각각 시간을 재는 타이머들 초기화

        # 물뿌리개 타이머
        self.item_timer = QTimer(self.game_background_lb)
        self.item_timer.setInterval(1000)
        self.item_timer.timeout.connect(self.printTime)

        if self.which_btn == 1 and self.isBug == False and self.isDust == False:
            GrawingSeed.use_water += 1
            self.label_water.setText(str(GrawingSeed.use_water) + "번")

            try:
                self.btn_timer_flag = 0
                self.item_timer.start()  # 물뿌리개 타이머 시작
                self.btn_water.setEnabled(False)  # 물뿌리개 버튼 비활성화
                self.btn_pesticide.setEnabled(False)
                self.btn_umbrella.setEnabled(False)
                print("물뿌리개다!!")  # 디버깅용
                self.which_btn = 0
                self.setCursor(QtCore.Qt.PointingHandCursor)  # 커서 설정
                self.btn_water.setStyleSheet(
                    "background-image : url(./images/watering_false.png); border: 0px solid black;")
                self.btn_pesticide.setStyleSheet(
                    "background-image : url(./images/pesticide_false.png); border: 0px solid black;")
                self.btn_umbrella.setStyleSheet(
                    "background-image : url(./images/umbrella_false.png); border: 0px solid black;")

                if GrawingSeed.current_level == 1:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/first_stage_water.png); border: 0px solid black;")
                elif GrawingSeed.current_level == 2:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/second_stage_water.png); border: 0px solid black;")
                elif GrawingSeed.current_level == 3:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/third_stage_water.png); border: 0px solid black;")
                elif GrawingSeed.current_level == 4:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/last_stage_water.png); border: 0px solid black;")

            except:
                print("물뿌리개 에러---")

        elif self.which_btn == 2 and self.isBug == True:
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
                self.btn_water.setStyleSheet(
                    "background-image : url(./images/watering_false.png); border: 0px solid black;")
                self.btn_pesticide.setStyleSheet(
                    "background-image : url(./images/pesticide_false.png); border: 0px solid black;")
                self.btn_umbrella.setStyleSheet(
                    "background-image : url(./images/umbrella_false.png); border: 0px solid black;")

                self.bug_timer.stop()
                self.bug_time = 0

                self.bug_success += 1

                if GrawingSeed.current_level == 1:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/first_stage_pesticide.png); border: 0px solid black;")
                elif GrawingSeed.current_level == 2:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/second_stage_pesticide.png); border: 0px solid black;")
                elif GrawingSeed.current_level == 3:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/third_stage_pesticide.png); border: 0px solid black;")
                elif GrawingSeed.current_level == 4:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/last_stage_pesticide.png); border: 0px solid black;")

                self.isBug = False

            except:
                print("살충제 에러---")

        elif self.which_btn == 3 and self.isDust == True:
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
                self.btn_water.setStyleSheet(
                    "background-image : url(./images/watering_false.png); border: 0px solid black;")
                self.btn_pesticide.setStyleSheet(
                    "background-image : url(./images/pesticide_false.png); border: 0px solid black;")
                self.btn_umbrella.setStyleSheet(
                    "background-image : url(./images/umbrella_false.png); border: 0px solid black;")

                self.dust_timer.stop()
                self.dust_time = 0

                self.dust_success += 1

                if GrawingSeed.current_level == 1:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/first_stage_umbrella.png); border: 0px solid black;")
                elif GrawingSeed.current_level == 2:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/second_stage_umbrella.png); border: 0px solid black;")
                elif GrawingSeed.current_level == 3:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/third_stage_umbrella.png); border: 0px solid black;")
                elif GrawingSeed.current_level == 4:
                    self.btn_char.setStyleSheet(
                        "background-image : url(./images/last_stage_umbrella.png); border: 0px solid black;")

                self.isDust = False

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
        btn_return.clicked.connect(self.go_to_home)
        opacity_effect = QGraphicsOpacityEffect(btn_return)
        opacity_effect.setOpacity(0)
        btn_return.setGraphicsEffect(opacity_effect)

        self.main_background_lb.setVisible(False)
        self.rule_background_lb.setVisible(True)

    # 게임 기록 보기
    def show_game_record(self):
        pass
    
    # 게임 기록 하기
    def write_game_record(self):
        nickname, ok = QInputDialog.getText(self, '게임 기록', '닉네임 or 이름을 입력하세요')
        if ok:
            # 비속어 있는지 확인하기
            slang_file = open('./text/slang.txt', 'r', encoding='utf-8')
            slang_data = []
            while True:
                line = slang_file.readline()
                if not line:
                    break
                slang_data.append(line)
            slang_file.close()
            for slang_word in slang_data:
                slang_word = slang_word.split(",")
            if nickname not in slang_word:
                score_file = open('text/score.txt', 'a', encoding='utf-8')
                score_file.write(nickname + '\t' + str(self.score_label.text()) + '님\t' + str(self.star_count) + '개\n')
                score_file.close()
            else:
                q = QMessageBox(QMessageBox.Warning, "비속어 사용 감지", "비속어는 사용할 수 없습니다")
                q.setStandardButtons(QMessageBox.Ok);
                i = QIcon()
                i.addPixmap(QPixmap("./images/warn.png"), QIcon.Normal)
                q.setWindowIcon(i)
                q.exec_()
        else:
            pass
        slang_file.close()

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
    def go_to_home(self):
        self.main_background_lb.setVisible(True)
        self.game_success_lb.setVisible(False)

        self.dust_times = []
        self.dust_count = 0

    def none_item(self):
        reply = QMessageBox.question(self, '아이템 없음', '아이템을 선택해주세요', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return
        else:
            self.game_background_lb.setVisible(False)
            self.main_background_lb.setVisible(True)
            self.timer.stop()
            self.time = 0

            # 게임을 중단하고 메인으로 돌아갔을 때 메인화면 음악 재생
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(self.main_music_file)
            pygame.mixer.music.play(-1)

            self.dust_times = []
            self.dust_count = 0

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '게임 종료', '정말 게임을 종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.timer.stop()
            self.time = 0
        else:
            event.ignore()


# 실행하는 메인함수
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 애플리케이션 객체 생성
    ex = GrawingSeed()
    sys.exit(app.exec_())