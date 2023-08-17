import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import os

def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

svg_path = get_resource_path("1.svg")



class WeldTecBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set main window properties
        self.setWindowTitle("SecNet")
        self.setGeometry(100, 100, 800, 600)
        icon = QIcon("2.svg")  # Replace with your icon path
        self.setWindowIcon(icon)

        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Create navigation bar
        navigation_bar = QToolBar("Navigation")
        self.addToolBar(navigation_bar)

        # Add back button
        back_button = QAction("Back", self)
        back_button.triggered.connect(self.navigate_back)
        navigation_bar.addAction(back_button)

        # Add forward button
        forward_button = QAction("Forward", self)
        forward_button.triggered.connect(self.navigate_forward)
        navigation_bar.addAction(forward_button)

        # Add address bar
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.navigate_to_url)
        navigation_bar.addWidget(self.address_bar)

        # Add reload button
        reload_button = QAction("Reload", self)
        reload_button.triggered.connect(self.reload)
        navigation_bar.addAction(reload_button)

        # Create bookmark bar
        bookmark_bar = QToolBar("Bookmarks")
        self.addToolBar(bookmark_bar)

        searchtec_bookmark = QAction(QIcon("2.svg"), "SearchTec", self)
        searchtec_bookmark.triggered.connect(lambda: self.add_new_tab(QUrl("https://searchtec.tech")))
        bookmark_bar.addAction(searchtec_bookmark)
        searchtec_bookmark = QAction(QIcon("1.svg"), "YouTube", self)
        searchtec_bookmark.triggered.connect(lambda: self.add_new_tab(QUrl("https://joinpeertube.org/en_US/browse-content")))
        bookmark_bar.addAction(searchtec_bookmark)
        searchtec_bookmark = QAction(QIcon("3.svg"), "PoopShoot", self)
        searchtec_bookmark.triggered.connect(lambda: self.add_new_tab(QUrl("https://62.72.6.224")))
        bookmark_bar.addAction(searchtec_bookmark)

        # Set stylesheet for WeldTec theme
        self.setStyleSheet("background-color: black; color: yellow;")

        # Open default tab
        self.add_new_tab(QUrl("https://searchtec.tech"))

    def navigate_back(self):
        current_webview = self.tabs.currentWidget()
        current_webview.back()

    def navigate_forward(self):
        current_webview = self.tabs.currentWidget()
        current_webview.forward()

    def reload(self):
        current_webview = self.tabs.currentWidget()
        current_webview.reload()

    def navigate_to_url(self):
        url = self.address_bar.text()
        if not url.startswith('http'):
            url = 'http://' + url
        self.add_new_tab(QUrl(url))

    def add_new_tab(self, qurl):
        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.loadFinished.connect(lambda: self.set_tab_title(browser))
        i = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(i)

    def set_tab_title(self, browser):
        title = browser.page().title()
        index = self.tabs.indexOf(browser)
        self.tabs.setTabText(index, title)

    def close_tab(self, index):
        if self.tabs.count() < 2:
            self.close()
        else:
            self.tabs.removeTab(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = WeldTecBrowser()
    browser.show()
    sys.exit(app.exec_())

