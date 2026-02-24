# main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox, QHeaderView
from db_helper import DB, DB_CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("성심당 상품 관리")

        self.resize(800, 600)

        self.db = DB(**DB_CONFIG)

        # 중앙 위젯 및 레이아웃
        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)

        # 상단: 입력 폼 + 추가 버튼
        form_box = QHBoxLayout()
        self.input_name = QLineEdit()
        self.input_price = QLineEdit()
        self.input_num = QLineEdit()
        self.btn_add = QPushButton("추가")
        self.btn_add.clicked.connect(self.add_member)

        form_box.addWidget(QLabel("상품이름"))
        form_box.addWidget(self.input_name)
        form_box.addWidget(QLabel("가격"))
        form_box.addWidget(self.input_price)
        form_box.addWidget(QLabel("재고"))
        form_box.addWidget(self.input_num)
        form_box.addWidget(self.btn_add)

        # 수정
        self.btn_update = QPushButton("수정")  # 1. 버튼 객체 생성
        self.btn_update.clicked.connect(self.update_member)  # 2. 클릭 시 실행할 함수 연결

        # 수정 버튼 추가
        form_box.addWidget(self.btn_update)

        # 삭제
        self.btn_delete = QPushButton("삭제")
        self.btn_delete.clicked.connect(self.delete_member)

        # 삭제 버튼 추가
        form_box.addWidget(self.btn_delete)


        # 중앙: 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "상품이름", "가격", "재고"])
        self.table.setEditTriggers(self.table.NoEditTriggers)  # 표준 예시: 목록은 읽기 전용
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 배치
        vbox.addLayout(form_box)
        vbox.addWidget(self.table)

        # 초기 데이터 로드
        self.load_members()


    def load_members(self):
        rows = self.db.fetch_members()
        self.table.setRowCount(len(rows))
        for r, (mid, name, price, num) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(mid)))
            self.table.setItem(r, 1, QTableWidgetItem(name))
            self.table.setItem(r, 2, QTableWidgetItem(str(price)))
            self.table.setItem(r, 3, QTableWidgetItem(str(num)))
        # self.table.resizeColumnsToContents()

    def add_member(self):
        name = self.input_name.text().strip()
        price = self.input_price.text().strip()
        num = self.input_num.text().strip()
        if not name or not price or not num:
            QMessageBox.warning(self, "오류", "다시 입력하세요.")
            return

        price_int = int(price)
        num_int = int(num)


        ok = self.db.insert_member(name,price_int, num_int)
        if ok:
            QMessageBox.information(self, "완료", "추가되었습니다.")
            self.input_name.clear()
            self.input_price.clear()
            self.input_num.clear()
            self.load_members()
        else:
            QMessageBox.critical(self, "실패", "추가 중 오류가 발생했습니다.")


    def update_member(self):
        name = self.input_name.text().strip()
        price = self.input_price.text().strip()
        num = self.input_num.text().strip()

        price_int = int(price)
        num_int = int(num)

        ok = self.db.modify_member(price_int, num_int, name)
        if ok:
            QMessageBox.information(self, "완료", "수정되었습니다.")
            self.input_name.clear()
            self.input_price.clear()
            self.input_num.clear()
            self.load_members()
        else:
            QMessageBox.critical(self, "실패", "추가 중 오류가 발생했습니다.")


    def delete_member(self):
        name = self.input_name.text().strip()
        price = self.input_price.text().strip()
        num = self.input_num.text().strip()


        ok = self.db.err_member(name)
        if ok:
            QMessageBox.information(self, "완료", "삭제되었습니다.")
            #self.input_name.clear()
            self.load_members()
        else:
            QMessageBox.critical(self, "실패", "추가 중 오류가 발생했습니다.")