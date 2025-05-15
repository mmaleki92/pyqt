import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt


class CounterWidget(QWidget):
    # Custom signal declaration
    value_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create counter display
        self.counter_label = QLabel("0")
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.counter_label.setStyleSheet("font-size: 24pt;")
        layout.addWidget(self.counter_label)
        
        # Create buttons
        self.increment_button = QPushButton("Increment")
        self.decrement_button = QPushButton("Decrement")
        self.reset_button = QPushButton("Reset")
        
        layout.addWidget(self.increment_button)
        layout.addWidget(self.decrement_button)
        layout.addWidget(self.reset_button)
        
        # Connect buttons to slots
        self.increment_button.clicked.connect(self.increment)
        self.decrement_button.clicked.connect(self.decrement)
        self.reset_button.clicked.connect(self.reset)
        
        # Connect our custom signal to our update_label slot
        self.value_changed.connect(self.update_label)
        
        self.setLayout(layout)
    
    @pyqtSlot()
    def increment(self):
        self.counter += 1
        self.value_changed.emit(self.counter)  # Emit signal with new value
    
    @pyqtSlot()
    def decrement(self):
        self.counter -= 1
        self.value_changed.emit(self.counter)  # Emit signal with new value
    
    @pyqtSlot()
    def reset(self):
        self.counter = 0
        self.value_changed.emit(self.counter)  # Emit signal with new value
    
    @pyqtSlot(int)
    def update_label(self, value):
        self.counter_label.setText(str(value))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Counter Example - Signal/Slot")
        self.setGeometry(100, 100, 300, 200)
        
        # Set central widget
        self.counter_widget = CounterWidget()
        self.setCentralWidget(self.counter_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()