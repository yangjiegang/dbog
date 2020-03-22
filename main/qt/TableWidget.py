from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton, QLabel, QLineEdit, QHeaderView


class TableWidget(QWidget):
    control_signal = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)

    def init_ui(self, row_cnt, column_cnt, super_widget):
        self.table = QTableWidget(row_cnt, column_cnt, super_widget)
        # 列自适应宽度
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.dataTable.resizeColumnsToContents()
        self.__layout = QVBoxLayout(self)
        self.__layout.addWidget(self.table)
        self.setLayout(self.__layout)

    def set_page_controller(self, page):
        """自定义页码控制器"""
        self.control_layout = QHBoxLayout()
        homePage = QPushButton("First")
        prePage = QPushButton("<Prev")
        self.curPage = QLabel("1")
        nextPage = QPushButton("Next>")
        finalPage = QPushButton("Last")
        self.totalPageName = QLabel(" Total-")
        self.totalPageNum = QLabel(str(page))
        self.totalPageUnit = QLabel("-Page ")
        skipLable_0 = QLabel("Goto Page")
        self.skipPage = QLineEdit()
        # skipLabel_1 = QLabel("Page")
        confirmSkip = QPushButton("OK")
        homePage.clicked.connect(self.__home_page)
        prePage.clicked.connect(self.__pre_page)
        nextPage.clicked.connect(self.__next_page)
        finalPage.clicked.connect(self.__final_page)
        confirmSkip.clicked.connect(self.__confirm_skip)
        self.control_layout.addStretch(1)
        self.control_layout.addWidget(homePage)
        self.control_layout.addWidget(prePage)
        self.control_layout.addWidget(self.curPage)
        self.control_layout.addWidget(nextPage)
        self.control_layout.addWidget(finalPage)
        self.control_layout.addWidget(self.totalPageName)
        self.control_layout.addWidget(self.totalPageNum)
        self.control_layout.addWidget(self.totalPageUnit)
        self.control_layout.addWidget(skipLable_0)
        # self.control_layout.addWidget(skipLabel_1)
        self.control_layout.addWidget(self.skipPage)
        self.control_layout.addWidget(confirmSkip)
        self.control_layout.addStretch(1)
        self.__layout.addLayout(self.control_layout)
        # layout不同的比例区分大小
        self.__layout.setStretchFactor(self.table, 4)
        self.__layout.setStretchFactor(self.control_layout, 1)

    def __home_page(self):
        """点击First信号"""
        self.control_signal.emit(["home", self.curPage.text()])

    def __pre_page(self):
        """点击Previous信号"""
        self.control_signal.emit(["pre", self.curPage.text()])

    def __next_page(self):
        """点击Next信号"""
        self.control_signal.emit(["next", self.curPage.text()])

    def __final_page(self):
        """Last点击信号"""
        self.control_signal.emit(["final", self.curPage.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.control_signal.emit(["confirm", self.skipPage.text()])

    def show_total_page(self):
        """返回当前总页数"""
        return int(self.totalPageNum.text())
