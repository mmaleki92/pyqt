import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLineEdit, 
                            QVBoxLayout, QWidget, QPushButton, QHBoxLayout)
from PyQt6.QtWebEngineWidgets import QWebEngineView

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Simple PyQt6 Browser')
        self.setGeometry(100, 100, 1024, 768)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create navigation bar
        nav_bar = QHBoxLayout()
        
        # Back button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.navigate_back)
        nav_bar.addWidget(self.back_button)
        
        # Forward button
        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.navigate_forward)
        nav_bar.addWidget(self.forward_button)
        
        # Reload button
        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.reload_page)
        nav_bar.addWidget(self.reload_button)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)
        
        # Add navigation bar to main layout
        layout.addLayout(nav_bar)
        
        # Create web view
        self.browser = QWebEngineView()
        self.browser.loadFinished.connect(self.update_url)
        layout.addWidget(self.browser)
        
        # Load a default page
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_back(self):
        self.browser.back()

    def navigate_forward(self):
        self.browser.forward()

    def reload_page(self):
        self.browser.reload()

    def navigate_to_url(self):
        url = self.url_bar.text()
        
        # Add http:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        self.browser.setUrl(QUrl(url))

    def update_url(self):
        self.url_bar.setText(self.browser.url().toString())

def main():
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()