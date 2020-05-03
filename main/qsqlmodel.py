import time
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlTableModel,QSqlDatabase
class Ui_form(QWidget):
    def __init__(self):
        super(Ui_form,self).__init__()
        self.resize(1000,500)
        self.ver = QVBoxLayout(self)
        self.show_table()
        self.buton = QPushButton(self)
        self.buton.setText("ddd")
        self.buton.clicked.connect(self._show)
        self.ver.addWidget(self.buton)
    def model_table(self):#初始化QSqlDatabase的model
        self.db = QSqlDatabase.addDatabase('QSQLITE')#数据库类型
        self.db.setDatabaseName('../data_db/date_of_cj.db')#数据库的相对为宗旨
        self.db.open()
        # 设置订单表格
        self.model_order_1 = QSqlTableModel()
        self.model_order_1.setTable('date_of_order')#表名
        self.model_order_1.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_order_1.select()

    # 创建QTable_view视图
    def show_table(self):
        # 初始化model
        self.model_table()
        self.table_view_1 = QTableView(self)
        self.table_view_1.setModel(self.model_order_1)
        #由于在刷新控件上，已经close了Qtable_View，所以要重新show一次。
        self.table_view_1.show()
        self.ver.addWidget(self.table_view_1)
    def _show(self):
        cc = time.time()
        conn = sqlite3.connect("../data_db/date_of_cj.db", isolation_level=None)
        cosur = conn.cursor()
        cosur.execute("update date_of_order set id_state=('%s') WHERE ID=('%s')" % (cc,1))
        self.table_view_1.updateEditorData()
        # 先关闭首次创建的Qtable_view视图
        self.table_view_1.close()
        # 再次调用QTable_view显示函数
        self.show_table()
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Ui_form()
    form.show()
    sys.exit(app.exec_())