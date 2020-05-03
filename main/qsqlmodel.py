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
    def model_table(self):#��ʼ��QSqlDatabase��model
        self.db = QSqlDatabase.addDatabase('QSQLITE')#���ݿ�����
        self.db.setDatabaseName('../data_db/date_of_cj.db')#���ݿ�����Ϊ��ּ
        self.db.open()
        # ���ö������
        self.model_order_1 = QSqlTableModel()
        self.model_order_1.setTable('date_of_order')#����
        self.model_order_1.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_order_1.select()

    # ����QTable_view��ͼ
    def show_table(self):
        # ��ʼ��model
        self.model_table()
        self.table_view_1 = QTableView(self)
        self.table_view_1.setModel(self.model_order_1)
        #������ˢ�¿ؼ��ϣ��Ѿ�close��Qtable_View������Ҫ����showһ�Ρ�
        self.table_view_1.show()
        self.ver.addWidget(self.table_view_1)
    def _show(self):
        cc = time.time()
        conn = sqlite3.connect("../data_db/date_of_cj.db", isolation_level=None)
        cosur = conn.cursor()
        cosur.execute("update date_of_order set id_state=('%s') WHERE ID=('%s')" % (cc,1))
        self.table_view_1.updateEditorData()
        # �ȹر��״δ�����Qtable_view��ͼ
        self.table_view_1.close()
        # �ٴε���QTable_view��ʾ����
        self.show_table()
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Ui_form()
    form.show()
    sys.exit(app.exec_())