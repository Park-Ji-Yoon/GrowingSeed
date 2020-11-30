import sys
import warnings

from PySide2.QtWidgets import QApplication
from growing_seed.growing_seed_game import GrawingSeed

# 경고(경고 메시지) 무시
warnings.filterwarnings(action='ignore')

# 실행하는 메인함수
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 애플리케이션 객체 생성
    ex = GrawingSeed()
    sys.exit(app.exec_())