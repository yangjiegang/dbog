import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from main.qt.MainWindow import DBogUI


# main window
class DBogWindow(QMainWindow, DBogUI):
    def __init__(self, parent=None):
        super(DBogWindow, self).__init__(parent)
        self.setup_ui(self)


app = QApplication(sys.argv)
DBogWin = DBogWindow()
DBogWin.show()
sys.exit(app.exec_())
