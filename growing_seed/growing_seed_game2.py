import csv
import sys
import threading
import random
import warnings

from PySide2 import QtCore, QtGui
from PySide2.QtCore import QTimer, Qt
from PySide2.QtGui import QFont, QIcon, QPixmap
from PySide2.QtWidgets import *
import pygame
import pandas as pd
from pygame import mixer
from datetime import datetime

# 경고(경고 메시지) 무시
warnings.filterwarnings(action='ignore')


# 게임 클래스
class GrawingSeed(QWidget):
    use_water = 0  # 물뿌리개 사용 횟수
    use_pesticide = 0  # 살충제 사용 횟수
    use_umbrella = 0  # 우산 사용 횟수

    current_level = 0  # 현재 단계 (1~4)

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

        self.isWatering = False
        self.isPesticide = False
        self.isUmbrella = False

        self.bug_success = 0
        self.dust_success = 0

        self.change_dust = True

        self.remove_weed = 0

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
        main_background = QtGui.QPixmap("./images/main_background.png")  # 사진 넣을 pixmap
        self.main_background_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.main_background_lb.setPixmap(main_background)  # 메인 배경 사진의 pixmap설정

        self.record_background_lb = QLabel()  # 메인 배경 사진을 넣을 라벨
        self.rule_background_lb = QLabel()
        self.record_background_lb = QLabel()
        self.record_high_background_lb = QLabel()
        self.record_low_background_lb = QLabel()
        self.record_new_background_lb = QLabel()
        self.game_over_lb = QLabel()
        self.game_success_lb = QLabel()
        self.game_background_lb = QLabel()

        self.turtorial_1_lb = QLabel()
        self.turtorial_2_lb = QLabel()
        self.turtorial_3_lb = QLabel()
        self.minigame_lb = QLabel()

        self.dust_timer = QTimer()
        self.bug_timer = QTimer()

        # 아이콘 설정
        self.setWindowIcon(QIcon('./images/icon.png'))

        # 씨앗씨 이야기 보기 버튼
        siasi_story_btn = QPushButton("", self.main_background_lb)
        siasi_story_btn.setGeometry(320, 277, 280, 135)
        siasi_story_btn.clicked.connect(self.btn_turtorial_1)
        opacity_effect = QGraphicsOpacityEffect(siasi_story_btn)
        opacity_effect.setOpacity(0)
        siasi_story_btn.setGraphicsEffect(opacity_effect)

        # 게임 기록 버튼
        btn_record = QPushButton("", self.main_background_lb)
        btn_record.setGeometry(77, 472, 190, 85)
        btn_record.clicked.connect(self.btn_record_clicked)
        opacity_effect = QGraphicsOpacityEffect(btn_record)
        opacity_effect.setOpacity(0)
        btn_record.setGraphicsEffect(opacity_effect)

        # 게임 시작 버튼
        btn_start = QPushButton("", self.main_background_lb)
        btn_start.setGeometry(305, 472, 190, 85)
        btn_start.clicked.connect(self.btn_start_clicked)
        opacity_effect = QGraphicsOpacityEffect(btn_start)
        opacity_effect.setOpacity(0)
        btn_start.setGraphicsEffect(opacity_effect)

        # 게임 방법 버튼
        btn_rule = QPushButton("", self.main_background_lb)
        btn_rule.setGeometry(537, 472, 190, 85)
        btn_rule.clicked.connect(self.btn_rule_clicked)
        opacity_effect = QGraphicsOpacityEffect(btn_rule)
        opacity_effect.setOpacity(0)
        btn_rule.setGraphicsEffect(opacity_effect)

        # 메인 화면 창
        self.setWindowTitle("Growing Seed")  # 창 제목
        self.setFixedSize(800, 650)  # 창 사이즈 설정 및 고정 (크기 변환 불가능)
        self.center()  # 창을 가운데로 위치
        self.show()  # 창을 보여줌

    # 버튼 클릭 효과음
    def book_sound(self):
        self.book_sound_file = mixer.Sound('./music/book_sound.wav')
        self.book_sound_file.play()

    def btn_turtorial_1(self):
        self.book_sound()
        self.main_background_lb.setVisible(False)

        # 화면 설정
        self.turtorial_1_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        turtorial_1_background = QtGui.QPixmap("./images/tutorial_1.png")  # 사진 넣을 pixmap
        self.turtorial_1_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.turtorial_1_lb.setPixmap(turtorial_1_background)  # 메인 배경 사진의 pixmap설정

        # 다음으로 버튼
        btn_next = QPushButton("", self.turtorial_1_lb)
        btn_next.setGeometry(608, 440, 100, 32)
        btn_next.clicked.connect(self.btn_turtorial_2)
        opacity_effect = QGraphicsOpacityEffect(btn_next)
        opacity_effect.setOpacity(0)
        btn_next.setGraphicsEffect(opacity_effect)

        # 뒤로가기 버튼
        btn_return = QPushButton("", self.turtorial_1_lb)
        btn_return.setGeometry(75, 55, 60, 60)
        btn_return.clicked.connect(self.go_to_home)
        opacity_effect = QGraphicsOpacityEffect(btn_return)
        opacity_effect.setOpacity(0)
        btn_return.setGraphicsEffect(opacity_effect)

        self.turtorial_1_lb.setVisible(True)

    def btn_turtorial_2(self):
        self.book_sound()
        self.turtorial_1_lb.setVisible(False)

        # 화면 설정
        self.turtorial_2_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        turtorial_2_background = QtGui.QPixmap("./images/tutorial_2.png")  # 사진 넣을 pixmap
        self.turtorial_2_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.turtorial_2_lb.setPixmap(turtorial_2_background)  # 메인 배경 사진의 pixmap설정

        # 다음으로 버튼
        btn_next = QPushButton("", self.turtorial_2_lb)
        btn_next.setGeometry(608, 440, 100, 32)
        btn_next.clicked.connect(self.mini_game)
        opacity_effect = QGraphicsOpacityEffect(btn_next)
        opacity_effect.setOpacity(0)
        btn_next.setGraphicsEffect(opacity_effect)

        # 뒤로가기 버튼
        btn_return = QPushButton("", self.turtorial_2_lb)
        btn_return.setGeometry(75, 55, 60, 60)
        btn_return.clicked.connect(self.go_to_home)
        opacity_effect = QGraphicsOpacityEffect(btn_return)
        opacity_effect.setOpacity(0)
        btn_return.setGraphicsEffect(opacity_effect)

        self.turtorial_2_lb.setVisible(True)

    def mini_game(self):
        self.book_sound()
        self.turtorial_2_lb.setVisible(False)

        # 화면 설정
        self.minigame_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        minigame_background = QtGui.QPixmap("./images/minigame.png")  # 사진 넣을 pixmap
        self.minigame_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.minigame_lb.setPixmap(minigame_background)  # 메인 배경 사진의 pixmap설정

        # 씨앗씨 버튼
        find_siasi = QPushButton("", self.minigame_lb)
        find_siasi.setGeometry(750, 255, 50, 65)
        find_siasi.clicked.connect(self.btn_turtorial_3)
        opacity_effect = QGraphicsOpacityEffect(find_siasi)
        opacity_effect.setOpacity(0)
        find_siasi.setGraphicsEffect(opacity_effect)

        # 다른 이모티콘 버튼
        find_fail1 = QPushButton("", self.minigame_lb)
        find_fail1.setGeometry(0, 150, 748, 500)
        find_fail1.clicked.connect(self.minigame_fail)
        opacity_effect = QGraphicsOpacityEffect(find_fail1)
        opacity_effect.setOpacity(0)
        find_fail1.setGraphicsEffect(opacity_effect)

        find_fail2 = QPushButton("", self.minigame_lb)
        find_fail2.setGeometry(748, 320, 52, 330)
        find_fail2.clicked.connect(self.minigame_fail)
        opacity_effect = QGraphicsOpacityEffect(find_fail2)
        opacity_effect.setOpacity(0)
        find_fail2.setGraphicsEffect(opacity_effect)

        # 뒤로가기 버튼
        btn_return = QPushButton("", self.minigame_lb)
        btn_return.setGeometry(75, 55, 60, 60)
        btn_return.clicked.connect(self.go_to_home)
        opacity_effect = QGraphicsOpacityEffect(btn_return)
        opacity_effect.setOpacity(0)
        btn_return.setGraphicsEffect(opacity_effect)

        self.minigame_lb.setVisible(True)

    def minigame_fail(self):
        fail_siasi_sound = mixer.Sound('./music/fail_siasi.mp3')
        fail_siasi_sound.play()

        msg = QMessageBox()
        msg.setText("다시 씨앗씨를 찾아보세요")
        msg.setWindowTitle("씨앗씨 찾기 실패")
        msg.setWindowIcon(QtGui.QIcon("./images/fail.png"))
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def btn_turtorial_3(self):
        find_siasi_sound = mixer.Sound('./music/find_siasi.mp3')
        find_siasi_sound.play()

        self.minigame_lb.setVisible(False)

        # 화면 설정
        self.turtorial_3_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        turtorial_3_background = QtGui.QPixmap("./images/tutorial_3.png")  # 사진 넣을 pixmap
        self.turtorial_3_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.turtorial_3_lb.setPixmap(turtorial_3_background)  # 메인 배경 사진의 pixmap설정

        # 홈으로 버튼
        go_home_btn = QPushButton("", self.turtorial_3_lb)
        go_home_btn.setGeometry(236, 560, 150, 70)
        go_home_btn.clicked.connect(self.go_to_home)
        opacity_effect = QGraphicsOpacityEffect(go_home_btn)
        opacity_effect.setOpacity(0)
        go_home_btn.setGraphicsEffect(opacity_effect)

        # 게임 시작 버튼
        strt_game_btn = QPushButton("", self.turtorial_3_lb)
        strt_game_btn.setGeometry(413, 560, 150, 70)
        strt_game_btn.clicked.connect(self.start_play_game)
        opacity_effect = QGraphicsOpacityEffect(strt_game_btn)
        opacity_effect.setOpacity(0)
        strt_game_btn.setGraphicsEffect(opacity_effect)

        # 뒤로가기 버튼
        btn_return = QPushButton("", self.turtorial_3_lb)
        btn_return.setGeometry(75, 55, 60, 60)
        btn_return.clicked.connect(self.go_to_home)
        opacity_effect = QGraphicsOpacityEffect(btn_return)
        opacity_effect.setOpacity(0)
        btn_return.setGraphicsEffect(opacity_effect)

        self.turtorial_3_lb.setVisible(True)

    # 게임 기록 버튼 이벤트
    def btn_record_clicked(self):
        self.btn_sound()
        self.show_game_record()

    # 버튼 클릭 효과음
    def btn_sound(self):
        self.sound_file = mixer.Sound('./music/btn_sound2.mp3')
        self.sound_file.play()

    # 게임 시작 버튼 이벤트
    def btn_start_clicked(self):
        self.btn_sound()
        self.start_play_game()

    # 게임 방법 버튼 이벤트
    def btn_rule_clicked(self):
        self.btn_sound()
        self.show_game_rule()

    # 창을 화면의 가운데로 옮겨주는 함수
    def center(self):

        qr = self.frameGeometry()  # 창의 위치와 크기 정보 가져와서 qr에 넣음
        cp = QDesktopWidget().availableGeometry().center()  # 사용하는 모니터 화면의 가운데 위치 파악
        qr.moveCenter(cp)  # 창의 위치를 화면의 중심으로 이동
        self.move(qr.topLeft())  # 현재 창을 qr의 위치로 이동시킴")

    def start_play_game(self):
        self.btn_sound()

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
        # 메인 노래 설정
        self.main_music_file = './music/main_music.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.main_music_file)
        pygame.mixer.music.play(-1)

        self.btn_sound()
        self.game_background_lb.setVisible(False)
        self.game_over_lb.setVisible(False)
        self.main_background_lb.setVisible(True)

    # 게임 오버 화면
    def game_over(self):
        self.timer.stop()
        self.time = 0
        self.bug_timer.stop()
        self.bug_time = 0
        self.dust_timer.stop()
        self.dust_time = 0

        game_over_sound = mixer.Sound('./music/game_over_sound2.mp3')
        game_over_sound.play()

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

        # 아이템 사용 횟수 0으로 초기화
        self.use_water = 0
        self.use_pesticide = 0
        self.use_umbrella = 0

        self.dust_times = []
        self.dust_count = 0

        self.remove_weed = 0

    # 씨앗씨 키우기 성공 화면
    def game_success(self):
        game_success_sound = mixer.Sound('./music/game_success_sound1.mp3')
        game_success_sound.play()

        # 점수 계산 함수 호출
        score_result = self.mark_score()

        # 보너스 점수 초기화
        bonus = 0

        # 별 갯수 초기화
        self.star_count = 0

        # 게임 변수 초기화
        self.timer.stop()
        self.time = 0
        self.bug_timer.stop()
        self.bug_time = 0
        self.dust_timer.stop()
        self.dust_time = 0
        self.weed_count = 0
        self.remove_weed = 0

        self.game_success_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨

        # 점수 라벨
        self.score_label = QLabel("0점", self.game_success_lb)
        self.score_label.setGeometry(100, 180, 700, 300)
        self.score_label.setFont(QFont('JalnanOTF', 60))
        self.score_label.setAlignment(QtCore.Qt.AlignVCenter)

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
        elif score_result <= 2000:
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
        self.score = self.use_water * 8 + self.bug_success * 13 + self.dust_success * 13 + (
                    120 - self.time) * 8 + self.remove_weed * 10
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

        # self.game_over()

        # 환경 오염 발생 준비
        self.dust_times = []  # 환경 오염이 발생할 시간 담을 list
        self.dust_count = random.randint(2, 4)  # 환경 오염 발생 횟수
        rand_num = random.randrange(8, 70, 15)
        # 겹치지 않게 self.dust_count만큼 랜덤 숫자를 뽑음
        for i in range(self.dust_count):
            while rand_num in self.dust_times:
                rand_num = random.randrange(8, 70, 15)
            self.dust_times.append(rand_num)
        print("정렬 전 : " + str(self.dust_times))  # 디버깅용
        self.dust_times.sort()
        print("정렬 후 : " + str(self.dust_times))  # 디버깅용

        # 환경 오염 발생 준비
        self.bug_times = []  # 환경 오염이 발생할 시간 담을 list
        self.bug_count = random.randint(2, 4)  # 환경 오염 발생 횟수
        rand_num2 = random.randrange(1, 65, 15)
        # 겹치지 않게 self.dust_count만큼 랜덤 숫자를 뽑음
        for i in range(self.bug_count):
            while rand_num2 in self.bug_times:
                rand_num2 = random.randrange(1, 65, 15)
            self.bug_times.append(rand_num2)
        print("정렬 전 : " + str(self.bug_times))  # 디버깅용
        self.bug_times.sort()
        print("정렬 후 : " + str(self.bug_times))  # 디버깅용

        self.weed_count = 0

        # 잡초 버튼 1
        self.weed1 = QPushButton("", self.game_background_lb)
        self.weed1.setGeometry(random.randint(50, 200), random.randint(70, 600), 48, 48)
        self.weed1.clicked.connect(self.click_weed)
        self.weed1.setVisible(False)

        # 잡초 버튼 2
        self.weed2 = QPushButton("", self.game_background_lb)
        self.weed2.setGeometry(random.randint(550, 700), random.randint(70, 600), 48, 48)
        self.weed2.clicked.connect(self.click_weed)
        self.weed2.setVisible(False)

        # 잡초 버튼 3
        self.weed3 = QPushButton("", self.game_background_lb)
        self.weed3.setGeometry(random.randint(50, 200), random.randint(70, 600), 48, 48)
        self.weed3.clicked.connect(self.click_weed)
        self.weed3.setVisible(False)

        # 잡초 버튼 4
        self.weed4 = QPushButton("", self.game_background_lb)
        self.weed4.setGeometry(random.randint(550, 700), random.randint(70, 600), 48, 48)
        self.weed4.clicked.connect(self.click_weed)
        self.weed4.setVisible(False)

        # 잡초 버튼 5
        self.weed5 = QPushButton("", self.game_background_lb)
        self.weed5.setGeometry(random.randint(50, 200), random.randint(70, 600), 48, 48)
        self.weed5.clicked.connect(self.click_weed)
        self.weed5.setVisible(False)

        # 잡초 버튼 6
        self.weed6 = QPushButton("", self.game_background_lb)
        self.weed6.setGeometry(random.randint(550, 700), random.randint(70, 600), 48, 48)
        self.weed6.clicked.connect(self.click_weed)
        self.weed6.setVisible(False)

        # 잡초 버튼 7
        self.weed7 = QPushButton("", self.game_background_lb)
        self.weed7.setGeometry(random.randint(50, 200), random.randint(70, 600), 48, 48)
        self.weed7.clicked.connect(self.click_weed)
        self.weed7.setVisible(False)

        # 잡초 버튼 8
        self.weed8 = QPushButton("", self.game_background_lb)
        self.weed8.setGeometry(random.randint(550, 700), random.randint(70, 600), 48, 48)
        self.weed8.clicked.connect(self.click_weed)
        self.weed8.setVisible(False)

        # 잡초 버튼 9
        self.weed9 = QPushButton("", self.game_background_lb)
        self.weed9.setGeometry(random.randint(50, 200), random.randint(70, 600), 48, 48)
        self.weed9.clicked.connect(self.click_weed)
        self.weed9.setVisible(False)

        # 잡초 버튼 10
        self.weed10 = QPushButton("", self.game_background_lb)
        self.weed10.setGeometry(random.randint(550, 700), random.randint(70, 600), 48, 48)
        self.weed10.clicked.connect(self.click_weed)
        self.weed10.setVisible(False)

        # 잡초 버튼 11
        self.weed11 = QPushButton("", self.game_background_lb)
        self.weed11.setGeometry(random.randint(50, 200), random.randint(70, 600), 48, 48)
        self.weed11.clicked.connect(self.click_weed)
        self.weed11.setVisible(False)

        # 잡초 버튼 12
        self.weed12 = QPushButton("", self.game_background_lb)
        self.weed12.setGeometry(random.randint(550, 700), random.randint(70, 600), 48, 48)
        self.weed12.clicked.connect(self.click_weed)
        self.weed12.setVisible(False)

        # 잡초 버튼 13
        self.weed13 = QPushButton("", self.game_background_lb)
        self.weed13.setGeometry(random.randint(50, 200), random.randint(70, 600), 48, 48)
        self.weed13.clicked.connect(self.click_weed)
        self.weed13.setVisible(False)

        # 잡초 버튼 14
        self.weed14 = QPushButton("", self.game_background_lb)
        self.weed14.setGeometry(random.randint(550, 700), random.randint(70, 600), 48, 48)
        self.weed14.clicked.connect(self.click_weed)
        self.weed14.setVisible(False)

        # 잡초 버튼 15
        self.weed15 = QPushButton("", self.game_background_lb)
        self.weed15.setGeometry(random.randint(50, 200), random.randint(70, 600), 48, 48)
        self.weed15.clicked.connect(self.click_weed)
        self.weed15.setVisible(False)

        # 잡초 버튼 16
        self.weed16 = QPushButton("", self.game_background_lb)
        self.weed16.setGeometry(random.randint(550, 700), random.randint(70, 600), 48, 48)
        self.weed16.clicked.connect(self.click_weed)
        self.weed16.setVisible(False)

        # 잡초 버튼 17
        self.weed17 = QPushButton("", self.game_background_lb)
        self.weed17.setGeometry(random.randint(50, 200), random.randint(70, 600), 48, 48)
        self.weed17.clicked.connect(self.click_weed)
        self.weed17.setVisible(False)

        # 잡초 버튼 18
        self.weed18 = QPushButton("", self.game_background_lb)
        self.weed18.setGeometry(random.randint(550, 700), random.randint(70, 600), 48, 48)
        self.weed18.clicked.connect(self.click_weed)
        self.weed18.setVisible(False)

        # 잡초 버튼 19
        self.weed19 = QPushButton("", self.game_background_lb)
        self.weed19.setGeometry(random.randint(50, 200), random.randint(70, 600), 48, 48)
        self.weed19.clicked.connect(self.click_weed)
        self.weed19.setVisible(False)

        # 잡초 버튼 20
        self.weed20 = QPushButton("", self.game_background_lb)
        self.weed20.setGeometry(random.randint(550, 700), random.randint(70, 600), 48, 48)
        self.weed20.clicked.connect(self.click_weed)
        self.weed20.setVisible(False)

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
            if GrawingSeed.use_water >= 3 and self.bug_success >= 0 and self.dust_success >= 0:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/second_stage.png); border: 0px solid black;")
                GrawingSeed.current_level = 2

        elif level == 2:
            if GrawingSeed.use_water >= 5 and self.bug_success >= 0 and self.dust_success >= 0:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/third_stage.png); border: 0px solid black;")
                GrawingSeed.current_level = 3

        elif level == 3:
            if GrawingSeed.use_water >= 7 and self.bug_success >= 0 and self.dust_success >= 0:
                self.btn_char.setStyleSheet("background-image : url(./images/last_stage.png); border: 0px solid black;")
                GrawingSeed.current_level = 4

        elif level == 4:
            if GrawingSeed.use_water >= 9 and self.bug_success >= 2 and self.dust_success >= 2:
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

            self.bug_timer.stop()
            self.bug_time = 0

            self.dust_timer.stop()
            self.dust_time = 0

            self.weed_count = 0
            self.remove_weed = 0

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
            # if self.time % 10 == 5:
            #     self.bug(GrawingSeed.current_level)
            for j in self.bug_times:
                if j == self.time:
                    self.bug(GrawingSeed.current_level)
            # 게임 시작 시 설정한 시간마다 환경오염 발생
            for i in self.dust_times:
                if i == self.time:
                    self.dust(GrawingSeed.current_level)
            # 잡초 버튼 생성
            # (랜덤으로 위치값을 줌)
            if self.time % 10 == 0:
                self.weed_count += 1
                if self.weed_count == 1:
                    self.weed1.setVisible(True)
                    self.weed1.setStyleSheet("background-image : url(./images/weed_ver1.png); border: 0px solid black;")
                    self.weed2.setVisible(True)
                    self.weed2.setStyleSheet("background-image : url(./images/weed_ver2.png); border: 0px solid black;")
                    self.weed11.setVisible(True)
                    self.weed11.setStyleSheet("background-image : url(./images/weed_ver4.png); border: 0px solid black;")
                    self.weed12.setVisible(True)
                    self.weed12.setStyleSheet("background-image : url(./images/weed_ver5.png); border: 0px solid black;")
                    self.weed_count += 1
                elif self.weed_count == 2:
                    self.weed3.setVisible(True)
                    self.weed3.setStyleSheet("background-image : url(./images/weed_ver3.png); border: 0px solid black;")
                    self.weed4.setVisible(True)
                    self.weed4.setStyleSheet("background-image : url(./images/weed_ver1.png); border: 0px solid black;")
                    self.weed13.setVisible(True)
                    self.weed13.setStyleSheet("background-image : url(./images/weed_ver6.png); border: 0px solid black;")
                    self.weed14.setVisible(True)
                    self.weed14.setStyleSheet("background-image : url(./images/weed_ver4.png); border: 0px solid black;")
                    self.weed_count += 1
                elif self.weed_count == 3:
                    self.weed5.setVisible(True)
                    self.weed5.setStyleSheet("background-image : url(./images/weed_ver2.png); border: 0px solid black;")
                    self.weed6.setVisible(True)
                    self.weed6.setStyleSheet("background-image : url(./images/weed_ver3.png); border: 0px solid black;")
                    self.weed15.setVisible(True)
                    self.weed15.setStyleSheet("background-image : url(./images/weed_ver5.png); border: 0px solid black;")
                    self.weed16.setVisible(True)
                    self.weed16.setStyleSheet("background-image : url(./images/weed_ver6.png); border: 0px solid black;")
                    self.weed_count += 1
                elif self.weed_count == 4:
                    self.weed7.setVisible(True)
                    self.weed7.setStyleSheet("background-image : url(./images/weed_ver1.png); border: 0px solid black;")
                    self.weed8.setVisible(True)
                    self.weed8.setStyleSheet("background-image : url(./images/weed_ver2.png); border: 0px solid black;")
                    self.weed17.setVisible(True)
                    self.weed17.setStyleSheet("background-image : url(./images/weed_ver4.png); border: 0px solid black;")
                    self.weed18.setVisible(True)
                    self.weed18.setStyleSheet("background-image : url(./images/weed_ver5.png); border: 0px solid black;")
                    self.weed_count += 1
                elif self.weed_count == 5:
                    self.weed9.setVisible(True)
                    self.weed9.setStyleSheet("background-image : url(./images/weed_ver3.png); border: 0px solid black;")
                    self.weed10.setVisible(True)
                    self.weed10.setStyleSheet("background-image : url(./images/weed_ver1.png); border: 0px solid black;")
                    self.weed19.setVisible(True)
                    self.weed19.setStyleSheet("background-image : url(./images/weed_ver6.png); border: 0px solid black;")
                    self.weed20.setVisible(True)
                    self.weed20.setStyleSheet("background-image : url(./images/weed_ver4.png); border: 0px solid black;")
                    self.weed_count = 0

    # 잡초 클릭 이벤트
    def click_weed(self):
        send_weed_btn = self.sender()
        self.remove_weed += 1
        send_weed_btn.setVisible(False)

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
            self.game_over()
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
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/first_stage_dust.png); border: 0px solid black;")
                self.change_dust = False
            else:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/first_stage_acid.png); border: 0px solid black;")
                self.change_dust = True
        elif level == 2:
            if self.change_dust == True:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/second_stage_dust.png); border: 0px solid black;")
                self.change_dust = False
            else:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/second_stage_acid.png); border: 0px solid black;")
                self.change_dust = True
        elif level == 3:
            if self.change_dust == True:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/third_stage_dust.png); border: 0px solid black;")
                self.change_dust = False
            else:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/third_stage_acid.png); border: 0px solid black;")
                self.change_dust = True
        elif level == 4:
            if self.change_dust == True:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/last_stage_dust.png); border: 0px solid black;")
                self.change_dust = False
            else:
                self.btn_char.setStyleSheet(
                    "background-image : url(./images/last_stage_acid.png); border: 0px solid black;")
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
            self.game_over()
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

        if GrawingSeed.water_btn_time == 2 or GrawingSeed.pesticide_btn_time == 3 or GrawingSeed.umbrella_btn_time == 3:
            GrawingSeed.water_btn_time = 0
            GrawingSeed.pesticide_btn_time = 0
            GrawingSeed.umbrella_btn_time = 0
            self.btn_timer_flag = 4
            self.btn_water.setEnabled(True)  # 물뿌리개 버튼 활성화
            self.btn_pesticide.setEnabled(True)
            self.btn_umbrella.setEnabled(True)
            self.item_timer.stop()
            self.isWatering = False
            self.isPesticide = False
            self.isUmbrella = False
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
                self.isWatering = True
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
                self.isPesticide = True
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
                self.isUmbrella = True
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
        self.record_background_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        record_background_1 = QtGui.QPixmap("./images/record_basic.png")  # 사진 넣을 pixmap
        self.record_background_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.record_background_lb.setPixmap(record_background_1)  # 메인 배경 사진의 pixmap설정

        # 뒤로가기 버튼
        btn_return = QPushButton("", self.record_background_lb)
        btn_return.setGeometry(75, 55, 60, 60)
        btn_return.clicked.connect(self.go_to_home)
        opacity_effect = QGraphicsOpacityEffect(btn_return)
        opacity_effect.setOpacity(0)
        btn_return.setGraphicsEffect(opacity_effect)

        # 높은 점수 정렬 버튼
        btn_high_score = QPushButton("", self.record_background_lb)
        btn_high_score.setGeometry(85, 147, 180, 55)
        btn_high_score.clicked.connect(self.high_score)
        opacity_effect = QGraphicsOpacityEffect(btn_high_score)
        opacity_effect.setOpacity(0)
        btn_high_score.setGraphicsEffect(opacity_effect)

        # 낮은 점수 정렬 버튼
        btn_low_score = QPushButton("", self.record_background_lb)
        btn_low_score.setGeometry(311, 147, 180, 55)
        btn_low_score.clicked.connect(self.low_score)
        opacity_effect = QGraphicsOpacityEffect(btn_low_score)
        opacity_effect.setOpacity(0)
        btn_low_score.setGraphicsEffect(opacity_effect)

        # 최신순 점수 정렬 버튼
        btn_new_score = QPushButton("", self.record_background_lb)
        btn_new_score.setGeometry(537, 147, 180, 55)
        btn_new_score.clicked.connect(self.new_score)
        opacity_effect = QGraphicsOpacityEffect(btn_new_score)
        opacity_effect.setOpacity(0)
        btn_new_score.setGraphicsEffect(opacity_effect)

        self.main_background_lb.setVisible(False)
        self.record_background_lb.setVisible(True)

    def high_score(self):
        print("high score")

        self.record_background_lb.setVisible(False)
        self.record_low_background_lb.setVisible(False)
        self.record_new_background_lb.setVisible(False)

        self.record_high_background_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        record_background_1 = QtGui.QPixmap("./images/record_high.png")  # 사진 넣을 pixmap
        self.record_high_background_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.record_high_background_lb.setPixmap(record_background_1)  # 메인 배경 사진의 pixmap설정

        # 높은 점수 정렬 버튼
        btn_high_score = QPushButton("dd", self.record_high_background_lb)
        btn_high_score.setGeometry(85, 147, 180, 55)
        btn_high_score.clicked.connect(self.high_score)
        opacity_effect = QGraphicsOpacityEffect(btn_high_score)
        opacity_effect.setOpacity(0)
        btn_high_score.setGraphicsEffect(opacity_effect)

        # 낮은 점수 정렬 버튼
        btn_low_score = QPushButton("dd", self.record_high_background_lb)
        btn_low_score.setGeometry(311, 147, 180, 55)
        btn_low_score.clicked.connect(self.low_score)
        opacity_effect = QGraphicsOpacityEffect(btn_low_score)
        opacity_effect.setOpacity(0)
        btn_low_score.setGraphicsEffect(opacity_effect)

        # 최신순 점수 정렬 버튼
        btn_new_score = QPushButton("dd", self.record_high_background_lb)
        btn_new_score.setGeometry(537, 147, 180, 55)
        btn_new_score.clicked.connect(self.new_score)
        opacity_effect = QGraphicsOpacityEffect(btn_new_score)
        opacity_effect.setOpacity(0)
        btn_new_score.setGraphicsEffect(opacity_effect)

        # 뒤로가기 버튼
        btn_return = QPushButton("", self.record_high_background_lb)
        btn_return.setGeometry(75, 55, 60, 60)
        btn_return.clicked.connect(self.from_record_to_home)
        opacity_effect = QGraphicsOpacityEffect(btn_return)
        opacity_effect.setOpacity(0)
        btn_return.setGraphicsEffect(opacity_effect)

        # csv 파일
        df = pd.read_csv("./text/score.csv")  # csv파일 읽어보기
        df = df.sort_values(by=['score'], ascending=False)  # 점수 높은 순으로 정렬
        print(df)  # 디버깅용 출력

        # 높은 점수 순 scrollArea 선언
        high_scrollArea = QScrollArea(self.record_high_background_lb)
        high_scrollArea.setGeometry(82, 215, 640, 400)
        high_scrollArea.setStyleSheet("background-color: #ffe22f; color:#022c00;")

        # 정렬된 df를 string형으로 형변환 후 QLabel에 setText해줌
        high_scores = QLabel(str(df))
        high_scores.setGeometry(10, 5, 620, 390)
        high_scores.setAlignment(Qt.AlignHCenter)
        high_scores.setFont(QFont('JalnanOTF', 20))
        high_scrollArea.setWidget(high_scores)

        self.record_high_background_lb.setVisible(True)

    def low_score(self):
        print("low score")

        self.record_background_lb.setVisible(False)
        self.record_new_background_lb.setVisible(False)
        self.record_high_background_lb.setVisible(False)

        self.record_low_background_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        record_background_1 = QtGui.QPixmap("./images/record_low.png")  # 사진 넣을 pixmap
        self.record_low_background_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.record_low_background_lb.setPixmap(record_background_1)  # 메인 배경 사진의 pixmap설정

        # 높은 점수 정렬 버튼
        btn_high_score = QPushButton("", self.record_low_background_lb)
        btn_high_score.setGeometry(85, 147, 180, 55)
        btn_high_score.clicked.connect(self.high_score)
        opacity_effect = QGraphicsOpacityEffect(btn_high_score)
        opacity_effect.setOpacity(0)
        btn_high_score.setGraphicsEffect(opacity_effect)

        # 낮은 점수 정렬 버튼
        btn_low_score = QPushButton("", self.record_low_background_lb)
        btn_low_score.setGeometry(311, 147, 180, 55)
        btn_low_score.clicked.connect(self.low_score)
        opacity_effect = QGraphicsOpacityEffect(btn_low_score)
        opacity_effect.setOpacity(0)
        btn_low_score.setGraphicsEffect(opacity_effect)

        # 최신순 점수 정렬 버튼
        btn_new_score = QPushButton("", self.record_low_background_lb)
        btn_new_score.setGeometry(537, 147, 180, 55)
        btn_new_score.clicked.connect(self.new_score)
        opacity_effect = QGraphicsOpacityEffect(btn_new_score)
        opacity_effect.setOpacity(0)
        btn_new_score.setGraphicsEffect(opacity_effect)

        # 뒤로가기 버튼
        btn_return = QPushButton("", self.record_low_background_lb)
        btn_return.setGeometry(75, 55, 60, 60)
        btn_return.clicked.connect(self.from_record_to_home)
        opacity_effect = QGraphicsOpacityEffect(btn_return)
        opacity_effect.setOpacity(0)
        btn_return.setGraphicsEffect(opacity_effect)

        # csv 파일
        df = pd.read_csv("./text/score.csv")  # csv파일 읽어보기
        df = df.sort_values(by=['score'], ascending=True)  # 점수 낮은 순으로 정렬
        print(df)  # 디버깅용 출력

        # 낮은 점수 순 scrollArea 선언
        low_scrollArea = QScrollArea(self.record_low_background_lb)
        low_scrollArea.setGeometry(82, 215, 640, 400)
        low_scrollArea.setStyleSheet("background-color: #ffe22f; color:#022c00;")

        # 정렬된 df를 string형으로 형변환 후 QLabel에 setText해줌
        low_scores = QLabel(str(df))
        low_scores.setGeometry(10, 5, 620, 390)
        low_scores.setAlignment(Qt.AlignHCenter)
        low_scores.setFont(QFont('JalnanOTF', 20))
        low_scrollArea.setWidget(low_scores)

        self.record_low_background_lb.setVisible(True)

    def new_score(self):
        print("new score")

        self.record_background_lb.setVisible(False)
        self.record_low_background_lb.setVisible(False)
        self.record_high_background_lb.setVisible(False)

        self.record_new_background_lb = QLabel(self)  # 메인 배경 사진을 넣을 라벨
        record_background_1 = QtGui.QPixmap("./images/record_new.png")  # 사진 넣을 pixmap
        self.record_new_background_lb.resize(800, 650)  # 메인 배경 사진 라벨 사이즈
        self.record_new_background_lb.setPixmap(record_background_1)  # 메인 배경 사진의 pixmap설정

        # 높은 점수 정렬 버튼
        btn_high_score = QPushButton("", self.record_new_background_lb)
        btn_high_score.setGeometry(85, 147, 180, 55)
        btn_high_score.clicked.connect(self.high_score)
        opacity_effect = QGraphicsOpacityEffect(btn_high_score)
        opacity_effect.setOpacity(0)
        btn_high_score.setGraphicsEffect(opacity_effect)

        # 낮은 점수 정렬 버튼
        btn_low_score = QPushButton("", self.record_new_background_lb)
        btn_low_score.setGeometry(311, 147, 180, 55)
        btn_low_score.clicked.connect(self.low_score)
        opacity_effect = QGraphicsOpacityEffect(btn_low_score)
        opacity_effect.setOpacity(0)
        btn_low_score.setGraphicsEffect(opacity_effect)

        # 최신순 점수 정렬 버튼
        btn_new_score = QPushButton("", self.record_new_background_lb)
        btn_new_score.setGeometry(537, 147, 180, 55)
        btn_new_score.clicked.connect(self.new_score)
        opacity_effect = QGraphicsOpacityEffect(btn_new_score)
        opacity_effect.setOpacity(0)
        btn_new_score.setGraphicsEffect(opacity_effect)

        # 뒤로가기 버튼
        btn_return = QPushButton("", self.record_new_background_lb)
        btn_return.setGeometry(75, 55, 60, 60)
        btn_return.clicked.connect(self.from_record_to_home)
        opacity_effect = QGraphicsOpacityEffect(btn_return)
        opacity_effect.setOpacity(0)
        btn_return.setGraphicsEffect(opacity_effect)

        # csv 파일
        df = pd.read_csv("./text/score.csv")  # csv파일 읽어보기
        df = df.sort_values(by=['datetime'], ascending=False)  # 점수 낮은 순으로 정렬
        print(df)  # 디버깅용 출력

        # 최신순 scrollArea 선언
        new_scrollArea = QScrollArea(self.record_new_background_lb)
        new_scrollArea.setGeometry(82, 215, 640, 400)
        new_scrollArea.setStyleSheet("background-color: #ffe22f; color:#022c00;")

        # 정렬된 df를 string형으로 형변환 후 QLabel에 setText해줌
        new_scores = QLabel(str(df))
        new_scores.setGeometry(10, 5, 620, 390)
        new_scores.setAlignment(Qt.AlignHCenter)
        new_scores.setFont(QFont('JalnanOTF', 20))
        new_scrollArea.setWidget(new_scores)

        self.record_new_background_lb.setVisible(True)

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
                today = datetime.today()
                year = today.year
                month = today.month
                day = today.day
                hour = today.hour
                minute = today.minute
                current_time = str(year)[-2:] + str(month) + str(day) + str(hour) + str(minute)
                f = open('./text/score.csv', 'a', newline='', encoding="utf-8")
                wr = csv.writer(f)
                wr.writerow([self.star_count, nickname, self.score_label.text()[:-1], current_time])
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
        self.btn_sound()

        # 메인 노래 설정
        self.main_music_file = './music/main_music.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.main_music_file)
        pygame.mixer.music.play(-1)

        self.rule_background_lb.setVisible(False)
        self.record_background_lb.setVisible(False)
        self.record_high_background_lb.setVisible(False)
        self.record_low_background_lb.setVisible(False)
        self.record_new_background_lb.setVisible(False)
        self.main_background_lb.setVisible(True)
        self.game_success_lb.setVisible(False)
        self.game_background_lb.setVisible(False)

        self.turtorial_1_lb.setVisible(False)
        self.turtorial_2_lb.setVisible(False)
        self.turtorial_3_lb.setVisible(False)
        self.minigame_lb.setVisible(False)

        self.dust_times = []
        self.dust_count = 0

    def from_record_to_home(self):

        self.btn_sound()
        self.main_background_lb.setVisible(True)
        self.record_high_background_lb.setVisible(False)
        self.record_low_background_lb.setVisible(False)
        self.record_new_background_lb.setVisible(False)

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
            self.time = 0
        else:
            event.ignore()

# 경고(경고 메시지) 무시
warnings.filterwarnings(action='ignore')

# 실행하는 메인함수
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 애플리케이션 객체 생성
    ex = GrawingSeed()
    sys.exit(app.exec_())