import sys

# from PyQt4.QtGui import QApplication
# from PyQt4.QtCore import QUrl
# from PyQt4.QtWebKit import QWebView
# from PyQt5.QtGui import QLineEdit, QWidget,QTableWidget
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout, QTableWidget, QGridLayout
from PyQt5.QtNetwork import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView


class UrlInput(QLineEdit):
    def __init__(self, browser):
        print("-------UrlInput __init__----------")
        super(UrlInput, self).__init__()
        self.browser = browser
        # add event listener on "enter" pressed
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        print("-------UrlInput _return_pressed----------")
        url = QUrl(self.text())
        # load url into browser frame
        browser.load(url)


class RequestsTable(QTableWidget):
    header = ["url", "status", "content-type"]

    def __init__(self):
        print("-----------RequestsTable  __init__------------")
        super(RequestsTable, self).__init__()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(self.header)
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        # header.setResizeMode(QHeaderView.ResizeToContents)

    def update(self, data):
        print("-----------RequestsTable  update------------")
        last_row = self.rowCount()
        next_row = last_row + 1
        self.setRowCount(next_row)
        for col, dat in enumerate(data, 0):
            if not dat:
                continue
            self.setItem(last_row, col, QTableWidgetItem(dat))


class Manager(QNetworkAccessManager):
    def __init__(self, table):
        print("-------_finished--__init__-------")
        QNetworkAccessManager.__init__(self)
        # add event listener on "load finished" event
        self.finished.connect(self._finished)
        self.table = table

    def _finished(self, reply):
        # print("-------_finished---------")
        """Update table with headers, status code and url.
        """
        headers = reply.rawHeaderPairs()
        headers = {str(k): str(v) for k, v in headers}
        content_type = headers.get("Content-Type")
        url = reply.url().toString()
        # getting status is bit of a pain
        status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        print("-----------------------------")
        # status, ok = status#.toInt()
        # print(status,ok)
        print([url, str(status), content_type])
        # self.table.update([url, str(status), content_type])


class JavaScriptEvaluator(QLineEdit):
    def __init__(self, page):
        print("----------JavaScriptEvaluator init------------")
        super(JavaScriptEvaluator, self).__init__()
        self.page = page
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        print("--------JavaScriptEvaluator  _return_pressed-------------")
        frame = self.page.currentFrame()
        result = frame.evaluateJavaScript(self.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    grid = QGridLayout()
    browser = QWebEngineView()
    url_input = UrlInput(browser)
    requests_table = RequestsTable()

    manager = Manager(requests_table)
    # to tell browser to use network access manager
    # you need to create instance of QWebPage
    # page = QWebPage()
    # page.setNetworkAccessManager(manager)

    # browser.setPage(page)
    browser.load(QUrl(url_input.text()))

    js_eval = JavaScriptEvaluator(browser.page())

    grid.addWidget(url_input, 1, 0)
    grid.addWidget(browser, 2, 0)
    grid.addWidget(requests_table, 3, 0)
    grid.addWidget(js_eval, 4, 0)
    # text=browser.page().currentFrame().documentElement().toInnerXml()
    page = browser.page()
    # page.toPlainText()
    main_frame = QWidget()
    main_frame.setLayout(grid)
    main_frame.show()

    sys.exit(app.exec_())
# data = self.webView.page().currentFrame().documentElement().toInnerXml()
