from PyQt5 import QtCore
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, \
    QStackedWidget, QPushButton, QLabel, QMenuBar, QAction, QStatusBar, QTableWidgetItem, QTreeWidget, QTreeWidgetItem, \
    QMessageBox, QLineEdit, QComboBox

import main.qt.Vars as mVars
from main.qt.MySQLHandler import MyDBHandler
from main.qt.SqlTranslator import SqlTranslator
from main.qt.TableWidget import TableWidget
from main.qt.Tools import CTools, cTool


# main window
class DBogUI(object):
    def __init__(self):
        self.db_handler = MyDBHandler()
        self.sqlTranslator = SqlTranslator()
        self.page_size = 10
        self.former_table_data = []
        self.current_table_data = []
        self.changedTableData = []
        self.cell_editable_flg = 0
        self.mainWidget = None
        self.centerLayout = None
        self.stackedWidget = None
        self.statusbar = None
        self.data_page = None
        self.data_page_layout = None
        self.menubar = None
        self.dataPanel = None
        self.data_panel_layout = None
        self.sqlTextEdit = None
        self.table_widget = None
        self.btn_panel = None
        self.btn_panel_layout = None
        self.addLnBtn = None
        self.rmvLnBtn = None
        self.queryBtn = None
        self.editBtn = None
        self.saveBtn = None
        self.treePanel = None
        self.treePanelLayout = None
        self.tableTree = None
        self.translate_page = None
        self.translate_page_layout = None
        self.translate_up_panel = None
        self.translate_up_panel_layout = None
        self.src_sql_text_edit = None
        self.dest_sql_text_edit = None
        self.translate_down_panel = None
        self.translate_down_panel_layout = None
        self.from_sql_type_combobox = None
        self.to_sql_type_combobox = None
        self.translate_btn = None
        self.swap_btn = None
        self.clear_btn = None
        self.login_page = None
        self.usmLabel = None
        self.unmTextEdit = None
        self.pwdLabel = None
        self.pwdTextEdit = None
        self.hostLabel = None
        self.hostTextEdit = None
        self.dbNameLabel = None
        self.dbNameTextEdit = None
        self.cnntDbBtn = None
        self.load_cfg_btn = None
        self.error_widgets = []
        self.plain_color = None

    # setup UI
    def setup_ui(self, MainWindow):
        # UI MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        # center widgets
        self.mainWidget = QWidget(MainWindow)
        # 设置字体
        self.mainWidget.setFont(QFont("Roman times", 11))
        self.mainWidget.setObjectName("mainWidget")
        MainWindow.setCentralWidget(self.mainWidget)
        self.centerLayout = QVBoxLayout(self.mainWidget)
        # 设置stacked widget
        self.stackedWidget = QStackedWidget(self.mainWidget)
        self.centerLayout.addWidget(self.stackedWidget)
        # 设置data page
        self.build_data_page()
        # layout不同的比例区分大小
        self.data_page_layout.setStretchFactor(self.dataPanel, 4)
        self.data_page_layout.setStretchFactor(self.treePanel, 1)
        # 设置login面板
        self.build_login_page()
        # 设置translate面板
        self.build_translate_page()
        # 将三个面板，加入stackedWidget
        self.stackedWidget.addWidget(self.data_page)
        self.stackedWidget.addWidget(self.login_page)
        self.stackedWidget.addWidget(self.translate_page)
        # menu
        self.build_menu_bar(MainWindow)
        # status bar
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # 刷新
        self.re_translate_ui(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        # refresh tree list
        self.db_handler.config(None, None, None, None)
        self.paint_tree()

    # data page
    def build_data_page(self):
        self.data_page = QWidget(self.mainWidget)
        self.centerLayout.addWidget(self.data_page)
        self.data_page_layout = QHBoxLayout(self.data_page)
        # 设置data面板
        self.build_tree_panel()
        # 设置data面板
        self.build_data_panel()
        # set event
        self.set_data_page_event()

    # menu
    def build_menu_bar(self, MainWindow):
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 400, 50))
        self.menubar.move(100, 100)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # 创建一个事件和一个特定图标
        show_data_action = QAction(QIcon('../resources/icon/database.png'), 'Operate', self)
        # show_data_action.setShortcut('Ctrl+Q')  # 设置事件的快捷方式
        show_data_action.setStatusTip('show data panel')  # 设置事件的状态提示
        show_data_action.triggered.connect(lambda: self.switch_page(0))  # 事件的触发
        login_menu = self.menubar.addMenu('&Data')  # 添加菜单file
        login_menu.addAction(show_data_action)  # 菜单添加事件
        # 创建一个事件和一个特定图标
        show_login_action = QAction(QIcon('../resources/icon/configure.png'), 'Config', self)
        # show_login_action.setShortcut('Ctrl+P')  # 设置事件的快捷方式
        show_login_action.setStatusTip('show login panel')  # 设置事件的状态提示
        show_login_action.triggered.connect(lambda: self.switch_page(1))  # 事件的触发
        login_menu = self.menubar.addMenu('&Login')  # 添加菜单file
        login_menu.addAction(show_login_action)  # 菜单添加事件
        # 创建一个事件和一个特定图标
        show_translate_action = QAction(QIcon('../resources/icon/translate.png'), 'Translate', self)
        # show_login_action.setShortcut('Ctrl+P')  # 设置事件的快捷方式
        show_translate_action.setStatusTip('show translate page')  # 设置事件的状态提示
        show_translate_action.triggered.connect(lambda: self.switch_page(2))  # 事件的触发
        translate_menu = self.menubar.addMenu('&Translate')  # 添加菜单file
        translate_menu.addAction(show_translate_action)  # 菜单添加事件

    # 设置data面板
    def build_data_panel(self):
        # data panel
        self.dataPanel = QWidget(self.data_page)
        self.data_page_layout.addWidget(self.dataPanel)
        self.data_panel_layout = QVBoxLayout(self.dataPanel)
        # SQL输入框
        self.sqlTextEdit = QTextEdit(self.dataPanel)
        self.sqlTextEdit.setObjectName("textEdit")
        # self.sqlTextEdit.setText("Enter your SQL here...")
        self.data_panel_layout.addWidget(self.sqlTextEdit)
        # 数据表格
        self.table_widget = TableWidget(self.dataPanel)
        self.table_widget.init_ui(0, 0, self.dataPanel)
        self.table_widget.set_page_controller(0)  # 表格设置页码控制
        self.table_widget.control_signal.connect(self.control_page)
        self.table_widget.setFixedSize(700, 400)
        self.data_panel_layout.addWidget(self.table_widget)
        # build inside panel
        self.build_btn_panel()
        self.data_panel_layout.setStretchFactor(self.sqlTextEdit, 2)
        self.data_panel_layout.setStretchFactor(self.table_widget, 6)
        self.data_panel_layout.setStretchFactor(self.btn_panel, 2)

    # button panel
    def build_btn_panel(self):
        # button panel
        self.btn_panel = QWidget(self.data_page)
        self.btn_panel.setFont(QFont("YaHei", 10))
        self.data_panel_layout.addWidget(self.btn_panel)
        self.btn_panel_layout = QHBoxLayout(self.btn_panel)
        # 表格操作：增加数据行按钮
        self.addLnBtn = QPushButton(self.btn_panel)
        self.addLnBtn.setMaximumSize(100, 80)
        self.addLnBtn.setObjectName("addLineButton")
        self.btn_panel_layout.addWidget(self.addLnBtn)
        # 表格操作：增加数据行按钮
        self.rmvLnBtn = QPushButton(self.btn_panel)
        self.rmvLnBtn.setObjectName("rmvLineButton")
        self.btn_panel_layout.addWidget(self.rmvLnBtn)
        # 查询按钮
        self.queryBtn = QPushButton(self.btn_panel)
        # self.queryBtn.setGeometry(QRect(150, 500, 100, 50))
        self.queryBtn.setObjectName("QueryButton")
        self.btn_panel_layout.addWidget(self.queryBtn)
        # 更新按钮
        self.editBtn = QPushButton(self.btn_panel)
        # self.editBtn.setGeometry(QRect(150, 500, 100, 50))
        self.editBtn.setObjectName("EditButton")
        self.btn_panel_layout.addWidget(self.editBtn)
        # 保存按钮
        self.saveBtn = QPushButton(self.btn_panel)
        # self.saveBtn.setGeometry(QRect(225, 500, 100, 50))
        self.saveBtn.setObjectName("SaveButton")
        self.btn_panel_layout.addWidget(self.saveBtn)
        # set partition / relative size
        self.btn_panel_layout.setStretchFactor(self.addLnBtn, 1)
        self.btn_panel_layout.setStretchFactor(self.rmvLnBtn, 1)
        self.btn_panel_layout.setStretchFactor(self.queryBtn, 1)
        self.btn_panel_layout.setStretchFactor(self.editBtn, 1)
        self.btn_panel_layout.setStretchFactor(self.saveBtn, 1)

    # left catalog tree panel
    def build_tree_panel(self):
        self.treePanel = QWidget(self.data_page)
        self.treePanel.setFont(QFont("SimHei", 11))
        self.treePanelLayout = QVBoxLayout(self.treePanel)
        # self.treePanel.setGeometry(QRect(0, 0, 100, 600))
        self.data_page_layout.addWidget(self.treePanel)
        # tableTree list
        self.tableTree = QTreeWidget(self.treePanel)
        self.treePanelLayout.addWidget(self.tableTree)
        # 设置列数
        self.tableTree.setColumnCount(1)
        self.tableTree.setColumnWidth(0, 100)
        # 设置头的标题
        self.tableTree.setHeaderLabel('Table List')
        # 绑定点击事件
        self.tableTree.clicked.connect(self.on_tree_clicked)

    # 加载树形菜单
    def paint_tree(self):
        if not CTools.isEmpty(self.db_handler.db_name):
            self.tableTree.clear()
            self.sqlTextEdit.setText("use %s;show tables;" % self.db_handler.db_name)
            table_lst = self.show_tables()
            # repaint tree nodes
            root = QTreeWidgetItem(self.tableTree)
            root.setText(0, self.db_handler.db_name)
            for i in range(len(table_lst)):
                table_name = table_lst[i]
                table_node = QTreeWidgetItem(root)
                table_node.setText(0, table_name)
            self.tableTree.addTopLevelItem(root)

    # data page
    def build_translate_page(self):
        self.translate_page = QWidget(self.mainWidget)
        self.centerLayout.addWidget(self.translate_page)
        self.translate_page_layout = QVBoxLayout(self.translate_page)
        self.build_translate_panel()

    # 设置data面板
    def build_translate_panel(self):
        # translate panel
        self.translate_up_panel = QWidget(self.translate_page)
        self.translate_page_layout.addWidget(self.translate_up_panel)
        # append widget
        self.translate_up_panel_layout = QHBoxLayout(self.translate_up_panel)
        # SQL输入框
        self.src_sql_text_edit = QTextEdit(self.translate_up_panel)
        self.src_sql_text_edit.setObjectName("src_sql_text_edit")
        self.src_sql_text_edit.setText("Enter source SQL to translate here...")
        self.translate_up_panel_layout.addWidget(self.src_sql_text_edit)
        # SQL输入框
        self.dest_sql_text_edit = QTextEdit(self.translate_up_panel)
        self.dest_sql_text_edit.setObjectName("dest_sql_text_edit")
        self.dest_sql_text_edit.setText("SQL translate result will be placed here...")
        self.dest_sql_text_edit.setReadOnly(True)
        self.translate_up_panel_layout.addWidget(self.dest_sql_text_edit)
        # translate panel
        self.translate_down_panel = QWidget(self.translate_page)
        self.translate_page_layout.addWidget(self.translate_down_panel)
        # append widget
        self.translate_down_panel_layout = QHBoxLayout(self.translate_down_panel)
        # select from sql type
        self.from_sql_type_combobox = QComboBox(self.translate_down_panel)
        self.from_sql_type_combobox.setMaximumSize(150, 120)
        self.from_sql_type_combobox.setObjectName("from_sql_type_combobox")
        self.from_sql_type_combobox.addItems(self.sqlTranslator.valid_from_dialect)
        self.translate_down_panel_layout.addWidget(self.from_sql_type_combobox)
        self.plain_color = self.from_sql_type_combobox.palette().color(QPalette.Background).toRgb()
        # select to sql type
        self.to_sql_type_combobox = QComboBox(self.translate_down_panel)
        self.to_sql_type_combobox.setMaximumSize(150, 120)
        self.to_sql_type_combobox.setObjectName("to_sql_type_combobox")
        # self.to_sql_type_combobox.addItems(['', 'mssql', 'sqlserver', 'mssqlserver', 'mysql', 'oracle', 'db2', 'db2udb'])
        self.to_sql_type_combobox.addItems(self.sqlTranslator.valid_to_dialect)
        self.translate_down_panel_layout.addWidget(self.to_sql_type_combobox)
        # translate按钮
        self.translate_btn = QPushButton(self.translate_down_panel)
        self.translate_btn.setMaximumSize(150, 120)
        self.translate_btn.setObjectName("Translate")
        self.translate_btn.setText("Translate")
        self.translate_down_panel_layout.addWidget(self.translate_btn)
        self.translate_btn.clicked.connect(self.on_translate)
        # 交换按钮
        self.swap_btn = QPushButton(self.translate_down_panel)
        self.swap_btn.setMaximumSize(150, 120)
        self.swap_btn.setObjectName("Swap")
        self.swap_btn.setText("Swap")
        self.translate_down_panel_layout.addWidget(self.swap_btn)
        self.swap_btn.clicked.connect(self.on_swap)
        # 清空按钮
        self.clear_btn = QPushButton(self.translate_down_panel)
        self.clear_btn.setMaximumSize(150, 120)
        self.clear_btn.setObjectName("Clear")
        self.clear_btn.setText("Clear")
        self.translate_down_panel_layout.addWidget(self.clear_btn)
        self.clear_btn.clicked.connect(self.on_clear)

    def on_translate(self):
        src_sql_str = self.src_sql_text_edit.toPlainText()
        from_type = self.from_sql_type_combobox.currentText()
        to_type = self.to_sql_type_combobox.currentText()
        error_msg = ""
        if not src_sql_str or src_sql_str == "Enter source SQL to translate here...":
            error_msg += "source SQL should not be empty\n"
            self.src_sql_text_edit.setTextBackgroundColor(QColor(255, 0, 0, 255))
            self.error_widgets.append(self.src_sql_text_edit)
        else:
            if self.src_sql_text_edit in self.error_widgets:
                self.error_widgets.remove(self.src_sql_text_edit)
        if not from_type:
            error_msg += "from SQL Type should not be empty\n"
            self.from_sql_type_combobox.setStyleSheet("QComboBox{color: rgb(255,0,0,255)}")
            self.error_widgets.append(self.from_sql_type_combobox)
        else:
            if self.from_sql_type_combobox in self.error_widgets:
                self.error_widgets.remove(self.from_sql_type_combobox)
        if not to_type:
            error_msg += "to SQL Type should not be empty\n"
            self.to_sql_type_combobox.setStyleSheet("QComboBox{color: rgb(255,0,0,255)}")
            self.error_widgets.append(self.to_sql_type_combobox)
        else:
            if self.to_sql_type_combobox in self.error_widgets:
                self.error_widgets.remove(self.to_sql_type_combobox)
        if self.error_widgets:
            QMessageBox.warning(None, "Warning", error_msg)
            return
        if self.src_sql_text_edit in self.error_widgets:
            self.src_sql_text_edit.setTextBackgroundColor(QColor(255, 255, 255, 255))
        if self.from_sql_type_combobox in self.error_widgets:
            self.from_sql_type_combobox.setStyleSheet("QComboBox{color: rgb%s}" % str(self.plain_color.getRgb()))
        if self.to_sql_type_combobox in self.error_widgets:
            self.to_sql_type_combobox.setStyleSheet("QComboBox{color: rgb%s}" % str(self.plain_color.getRgb()))
        dest_sql_str = self.sqlTranslator.web_translate(src_sql_str, from_type, to_type)
        self.dest_sql_text_edit.setText(dest_sql_str)

    def on_swap(self):
        # origin
        # from_sql_type_index = self.from_sql_type_combobox.currentIndex()
        # to_sql_type_index = self.to_sql_type_combobox.currentIndex()
        from_sql_type_text = self.from_sql_type_combobox.currentText()
        to_sql_type_text = self.to_sql_type_combobox.currentText()
        src_sql_str = self.src_sql_text_edit.toPlainText()
        dest_sql_str = self.dest_sql_text_edit.toPlainText()
        # change content
        self.from_sql_type_combobox.setCurrentIndex(
            self.sqlTranslator.get_opposite_sql_type(from_sql_type_text, 'from'))
        self.to_sql_type_combobox.setCurrentIndex(self.sqlTranslator.get_opposite_sql_type(to_sql_type_text, 'to'))
        self.dest_sql_text_edit.setText(src_sql_str)
        self.src_sql_text_edit.setText(dest_sql_str)

    def on_clear(self):
        self.from_sql_type_combobox.setCurrentIndex(0)
        self.to_sql_type_combobox.setCurrentIndex(0)
        self.dest_sql_text_edit.setText("")
        self.src_sql_text_edit.setText("")

    # show data after clicking the menu item in tree
    def on_tree_clicked(self):
        item = self.tableTree.currentItem()
        table_name = item.text(0)
        # no response when click database label
        if table_name != self.db_handler.db_name:
            cTool.logger.info("switch to data of table, name: %s" % table_name)
            self.sqlTextEdit.setText("select * from %s limit %d;" % (table_name, self.page_size))
            self.do_query()

    # when press append record button
    def on_append_record(self, table_name, page_size):
        if self.is_cell_editable():
            self.sqlTextEdit.setText("select * from %s limit %d;" % (table_name, page_size))
            self.do_query()
        else:
            self.warn_action("Table is not allowed to append record now")

    # when action is fobidden
    def warn_action(self, err_msg="illegal action"):
        cTool.logger.info("%s" % err_msg)
        QMessageBox.warning(None, "Warning", err_msg)

    # when press remove record button
    def on_remove_record(self):
        if self.is_cell_editable():
            cell_item_list = self.table_widget.table.selectedItems()
            count = len(cell_item_list)
            row_num_set = set()
            for x in range(0, count):
                table_item = cell_item_list[x]
                row_num_set.add(self.table_widget.table.row(table_item))
            selected_pk_set = set(
                self.former_table_data[row_num][self.db_handler.def_pk_index] for row_num in row_num_set)
            self.db_handler.delete_sql = self.db_handler.buildDeleteSQL(self.db_handler.def_table_name,
                                                                        self.db_handler.def_pk_name,
                                                                        selected_pk_set)
            # rmv_cnt = self.db_handler.modifyRecords(delete_sql)
            # print("updated count is %d for SQL %s" % (rmv_cnt, delete_sql))
            # self.do_query()
            self.former_table_data = [former_row_data for former_row_data in
                                      self.former_table_data if
                                      former_row_data[self.db_handler.def_pk_index] not in selected_pk_set]
            self.update_table_data(self.former_table_data, self.db_handler.def_field_name_lst, False)
        else:
            self.warn_action("Table is not allowed to delete record now")

    # 设置login面板
    def build_login_page(self):
        # login panel
        self.login_page = QWidget(self.stackedWidget)
        self.login_page.setGeometry(QRect(100, 100, 600, 600))
        # self.login_page_layout = QVBoxLayout(self.login_page)
        # username label
        self.usmLabel = QLabel(self.login_page)
        self.usmLabel.setGeometry(QRect(100, 100, 150, 50))
        self.usmLabel.setText("username ")
        # self.login_page_layout.addWidget(self.usmLabel)
        # username input
        self.unmTextEdit = QLineEdit(self.login_page)
        self.unmTextEdit.setText("")
        self.unmTextEdit.setGeometry(QRect(300, 100, 450, 50))
        # self.login_page_layout.addWidget(self.unmTextEdit)
        # password label
        self.pwdLabel = QLabel(self.login_page)
        self.pwdLabel.setGeometry(QRect(100, 150, 150, 50))
        self.pwdLabel.setText("password ")
        # self.login_page_layout.addWidget(self.pwdLabel)
        # password input
        self.pwdTextEdit = QLineEdit(self.login_page)
        self.pwdTextEdit.setText("")
        self.pwdTextEdit.setGeometry(QRect(300, 150, 450, 50))
        # self.login_page_layout.addWidget(self.pwdTextEdit)
        # host label
        self.hostLabel = QLabel(self.login_page)
        self.hostLabel.setGeometry(QRect(100, 200, 120, 50))
        self.hostLabel.setText("host address ")
        # self.login_page_layout.addWidget(self.hostLabel)
        # host input
        self.hostTextEdit = QLineEdit(self.login_page)
        self.hostTextEdit.setText("")
        self.hostTextEdit.setGeometry(QRect(300, 200, 450, 50))
        # self.login_page_layout.addWidget(self.hostTextEdit)
        # database name label
        self.dbNameLabel = QLabel(self.login_page)
        self.dbNameLabel.setGeometry(QRect(100, 250, 150, 50))
        self.dbNameLabel.setText("database name ")
        # self.login_page_layout.addWidget(self.dbNameLabel)
        # database name input
        self.dbNameTextEdit = QLineEdit(self.login_page)
        self.dbNameTextEdit.setText("")
        self.dbNameTextEdit.setGeometry(QRect(300, 250, 450, 50))
        # self.login_page_layout.addWidget(self.dbNameTextEdit)
        # confirm to connect database
        self.cnntDbBtn = QPushButton(self.login_page)
        self.cnntDbBtn.setObjectName("DbButton")
        self.cnntDbBtn.setGeometry(QRect(100, 350, 300, 50))
        # self.login_page_layout.addWidget(self.cnntDbBtn)
        # connect database with config file
        self.load_cfg_btn = QPushButton(self.login_page)
        self.load_cfg_btn.setObjectName("LoadConfigButton")
        self.load_cfg_btn.setGeometry(QRect(450, 350, 300, 50))
        # self.login_page_layout.addWidget(self.load_cfg_btn)
        # set event
        self.set_login_panel()

    # build login panel
    def set_login_panel(self):
        self.cnntDbBtn.clicked.connect(self.cnnt_db)
        self.load_cfg_btn.clicked.connect(self.re_config_db)

    # connect to database
    def cnnt_db(self):
        unmStr = self.unmTextEdit.text()
        pwdStr = self.pwdTextEdit.text()
        hostStr = self.hostTextEdit.text()
        dbNameStr = self.dbNameTextEdit.text()
        self.db_handler.config(hostStr, unmStr, pwdStr, dbNameStr)
        self.paint_tree()
        self.switch_page(0)

    # connect to database with configuration file
    def re_config_db(self):
        self.db_handler.config(mVars.host, mVars.username, mVars.password, mVars.database_name)

    # set label text of widget
    def re_translate_ui(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DBog"))
        self.setWindowIcon(QIcon("../resources/icon/ball.ico"))
        self.queryBtn.setText(_translate("MainWindow", "Query"))
        self.editBtn.setText(_translate("MainWindow", "Edit"))
        self.saveBtn.setText(_translate("MainWindow", "Save"))
        self.cnntDbBtn.setText(_translate("MainWindow", "ConnectByInputConfiguration"))
        self.load_cfg_btn.setText(_translate("MainWindow", "LoadConfigurationFile"))
        self.addLnBtn.setText(_translate("MainWindow", "AppendRecord"))
        self.rmvLnBtn.setText(_translate("MainWindow", "RemoveRecord"))

    # set event of data page
    def set_data_page_event(self):
        self.queryBtn.clicked.connect(self.do_query)
        self.editBtn.clicked.connect(self.do_edit)
        self.saveBtn.clicked.connect(self.do_save)
        self.addLnBtn.clicked.connect(lambda: self.on_append_record(self.db_handler.def_table_name, self.page_size - 1))
        self.rmvLnBtn.clicked.connect(self.on_remove_record)

    # switch to another page
    def switch_page(self, pnIndex):
        self.stackedWidget.setCurrentIndex(int(pnIndex))

    # execute query action
    def do_query(self):
        cmd_str = self.sqlTextEdit.toPlainText().replace(";", "")
        # 获取数据
        result_set = self.db_handler.get_all_result(cmd_str)
        # 获取表结构定义
        self.db_handler.gen_filed_name_list()
        # withdraw former table data / cast value None to empty string
        self.former_table_data = [[str(item) if item else "" for item in row] for row in result_set]
        # change button status to enable or not
        self.change_btn_status()
        # fill in table with empty line
        self.refresh_table(cmd_str)
        cTool.logger.info("result set for %s is %s" % (
            cmd_str, ','.join([str(row_data) for row_data in result_set])))

    # change button status to enable or not
    def change_btn_status(self):
        if self.is_cell_editable():
            self.addLnBtn.setEnabled(True)
            self.rmvLnBtn.setEnabled(True)
            self.saveBtn.setEnabled(True)
        else:
            self.addLnBtn.setEnabled(False)
            self.rmvLnBtn.setEnabled(False)
            self.saveBtn.setEnabled(False)

    # refresh table widget
    def refresh_table(self, cmd_str):
        row_cnt = len(self.former_table_data)
        if row_cnt > 0:
            col_cnt = len(self.former_table_data[0])
            while row_cnt < self.page_size:
                self.former_table_data.append(["" for i in range(col_cnt)])
                row_cnt = row_cnt + 1
        # count record
        page_cnt = self.count_record(cmd_str)
        # refresh table
        self.update_table_data(self.former_table_data, self.db_handler.def_field_name_lst, True)
        # refresh table page
        self.refresh_table_pager(page_cnt)

    # execute count of record
    def count_record(self, cmd_str):
        if "limit" in cmd_str:
            cmd_str = cmd_str.split("limit")[0]
        cnt_sql = "select count(1) from (%s) sub" % cmd_str
        ret_cnt = self.db_handler.get_single_result(cnt_sql)
        page_cnt = 0
        if ret_cnt and len(ret_cnt) > 0:
            ret_cnt = int(ret_cnt[0])
            page_cnt = int(ret_cnt / 10)
            if page_cnt % 10 != 0:
                page_cnt = page_cnt + 1
        return page_cnt

    # make new name of each field
    def rename_fields(self):
        ret_dict = self.count_list(self.db_handler.def_field_name_lst)
        for field_name in self.db_handler.def_field_name_lst:
            if ret_dict[field_name] > 1:
                field_name = "%s_%d" % (field_name, ret_dict[field_name])
                ret_dict[field_name] = ret_dict[field_name] - 1

    # statistic item count in a list
    def count_list(self, target_lst):
        ret_dict = {}
        for i in set(target_lst):
            ret_dict[i] = target_lst.count(i)
        return ret_dict

    # show table of current database
    def show_tables(self):
        tables_sql = "show tables;"
        self.sqlTextEdit.setText(tables_sql)
        return [tbl_name_tp[0] for tbl_name_tp in self.db_handler.get_all_result(tables_sql)]

    # execute update
    def do_edit(self):
        cmd_str = self.sqlTextEdit.toPlainText()
        row_count = self.db_handler.modifyRecords(cmd_str)
        info_msg = "Edit finish, effected row count: %d" % row_count
        cTool.logger.info(info_msg)
        QMessageBox.information(self, "Info", info_msg)

    # @decorator()
    # execute save action
    def do_save(self):
        # edit result set of multi tables is forbidden
        if self.is_cell_editable():
            # clear first
            self.current_table_data.clear()
            row_count = self.table_widget.table.rowCount()
            column_count = self.table_widget.table.columnCount()
            for i in range(0, row_count):
                curRowData = []
                for j in range(0, column_count):
                    cellValStr = self.table_widget.table.item(i, j).text()
                    curRowData.append(cellValStr)
                self.current_table_data.append(curRowData)
            # assemble SQL from data
            deleteSQL = self.db_handler.delete_sql
            if deleteSQL:
                # reset to empty string
                self.db_handler.delete_sql = ""
            else:
                dataLst = self.get_delete_data()
                deleteSQL = self.db_handler.buildDeleteSQL(self.db_handler.def_table_name, self.db_handler.def_pk_name,
                                                           dataLst) if dataLst else ""
            cTool.logger.info(deleteSQL)
            dataLst = self.get_insert_data()
            insertSQL = self.db_handler.buildInsertSQL(self.db_handler.def_table_name, dataLst) if dataLst else ""
            cTool.logger.info(insertSQL)
            rmCnt = self.db_handler.modifyRecords(deleteSQL) if deleteSQL else 0
            inCnt = self.db_handler.modifyRecords(insertSQL) if insertSQL else 0
            info_msg = "Save finish, effect record count removed: %d,inserted: %d" % (rmCnt, inCnt)
            cTool.logger.info(info_msg)
            QMessageBox.information(self, "Info", info_msg)
        else:
            self.warn_action("Table is not allowed to update now")

    # is table cell item editable
    def is_cell_editable(self):
        self.cell_editable_flg = QtCore.Qt.ItemIsEnabled if self.db_handler.is_combine_sql else QtCore.Qt.ItemIsEditable
        return self.cell_editable_flg == 2

    # withdraw delete data
    def get_delete_data(self):
        fmrSet = set(map(lambda x: ",".join(x), self.former_table_data))
        curSet = set(map(lambda x: ",".join(x), self.current_table_data))
        diffSet = fmrSet.difference(curSet)
        return list(map(lambda diffStr: diffStr.split(",")[self.db_handler.def_pk_index], diffSet))

    # withdraw insert data
    def get_insert_data(self):
        curSet = set(map(lambda x: ",".join(x), self.current_table_data))
        fmrSet = set(map(lambda x: ",".join(x), self.former_table_data))
        diffSet = curSet.difference(fmrSet)
        return list(map(lambda diffStr: diffStr.split(","), diffSet))

    # update/refresh table data
    def update_table_data(self, matrix_data, fd_name_list, update_header_flg):
        row_cnt = len(matrix_data)
        col_cnt = len(matrix_data[0]) if len(matrix_data) > 0 and len(matrix_data[0]) > 0 else 0
        # refresh table model struct
        self.clear_table_data()
        # if update_header_flg:
        self.refresh_table_header(fd_name_list, row_cnt, col_cnt)
        # refresh table data
        for row_num in range(0, row_cnt):
            for col_num in range(0, col_cnt):
                cell_data = str(matrix_data[row_num][col_num]) if matrix_data[row_num][col_num] else ""
                # 设置表格内容(行， 列) 文字
                self.table_widget.table.setItem(row_num, col_num, QTableWidgetItem(cell_data))

    # update/refresh table header
    def refresh_table_header(self, fd_name_list, row_cnt, col_cnt):
        self.table_widget.table.setRowCount(row_cnt)
        self.table_widget.table.setColumnCount(col_cnt)
        self.table_widget.table.setHorizontalHeaderLabels(fd_name_list)

    # update/refresh table pager
    def refresh_table_pager(self, page_count):
        self.table_widget.totalPageNum.setText(str(page_count))

    # clear table data
    def clear_table_data(self):
        self.table_widget.table.setRowCount(0)
        self.table_widget.table.setColumnCount(0)

    # config table item
    def touch_table_item(self):
        flag = QtCore.Qt.ItemIsEnabled if self.db_handler.is_combine_sql else QtCore.Qt.ItemIsEditable
        col_cnt = self.table_widget.table.colorCount()
        row_cnt = self.table_widget.table.rowCount()
        for col_num in range(0, col_cnt):
            for row_num in range(0, row_cnt):
                QTableWidgetItem(self.table_widget.table.item(row_cnt, col_cnt)).setFlags(flag)
                # 设置第二列不可编辑
                # self.table_widget.table.setItemDelegateForColumn(col_num, EmptyDelegate(self))
                # self.table_widget.table.setItemDelegateForColumn(col_num, QTableWidget.itemDelegate())

    # control page
    def control_page(self, signal):
        total_page = self.table_widget.show_total_page()
        if "home" == signal[0]:
            self.table_widget.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.table_widget.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.table_widget.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.table_widget.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 0:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                return
            self.table_widget.curPage.setText(signal[1])
        self.change_table_content()  # 改变表格内容

    # change table pager and content
    def change_table_content(self):
        """根据当前页改变表格的内容"""
        cur_page = int(self.table_widget.curPage.text())
        # 每页默认十条数据
        cTool.logger.info("current page: %s" % cur_page)
        page_limit_sql = "limit %s, %s" % ((cur_page - 1) * 10, 10)
        query_sql = "select * from %s %s;" % (self.db_handler.def_table_name, page_limit_sql)
        self.sqlTextEdit.setText(query_sql)
        self.do_query()

# # main window
# class DBogWindow(QMainWindow, DBogUI):
#     def __init__(self, parent=None):
#         super(DBogWindow, self).__init__(parent)
#         self.setup_ui(self)
#
#
# # main method
# # if __name__ == '__main__':
# app = QApplication(sys.argv)
# DBogWin = DBogWindow()
# DBogWin.show()
# sys.exit(app.exec_())

# select exam.username from exam join roles on exam.role_id = roles.role_id limit 0, 10;
