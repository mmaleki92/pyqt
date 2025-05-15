import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QListWidget, QComboBox, QLabel, QHBoxLayout)
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject, Qt


class EventGenerator(QObject):
    """Class that generates different types of events"""
    # Define custom signals with different parameters
    info_event = pyqtSignal(str, str)  # message, timestamp
    warning_event = pyqtSignal(str, str, int)  # message, timestamp, priority
    error_event = pyqtSignal(str, str, int, str)  # message, timestamp, code, source
    
    def __init__(self):
        super().__init__()
    
    def generate_info(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.info_event.emit(message, timestamp)
    
    def generate_warning(self, message, priority=1):
        timestamp = time.strftime("%H:%M:%S")
        self.warning_event.emit(message, timestamp, priority)
    
    def generate_error(self, message, code=404, source="system"):
        timestamp = time.strftime("%H:%M:%S")
        self.error_event.emit(message, timestamp, code, source)


class EventMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Create the event generator
        self.event_generator = EventGenerator()
        
        # Connect signals to slots
        self.event_generator.info_event.connect(self.on_info_event)
        self.event_generator.warning_event.connect(self.on_warning_event)
        self.event_generator.error_event.connect(self.on_error_event)
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Event type selection
        event_layout = QHBoxLayout()
        self.event_type = QComboBox()
        self.event_type.addItems(["Info", "Warning", "Error"])
        event_layout.addWidget(QLabel("Event Type:"))
        event_layout.addWidget(self.event_type)
        
        # Button to generate events
        self.generate_button = QPushButton("Generate Event")
        self.generate_button.clicked.connect(self.generate_event)
        event_layout.addWidget(self.generate_button)
        
        layout.addLayout(event_layout)
        
        # Event log
        self.event_list = QListWidget()
        layout.addWidget(QLabel("Event Log:"))
        layout.addWidget(self.event_list)
        
        # Clear button
        self.clear_button = QPushButton("Clear Log")
        self.clear_button.clicked.connect(self.event_list.clear)
        layout.addWidget(self.clear_button)
        
        self.setLayout(layout)
    
    def generate_event(self):
        """Generate an event based on the selected type"""
        event_type = self.event_type.currentText()
        
        if event_type == "Info":
            self.event_generator.generate_info("System is running normally")
        elif event_type == "Warning":
            self.event_generator.generate_warning("System resources are low", 2)
        else:  # Error
            self.event_generator.generate_error("Connection failed", 503, "network")
    
    @pyqtSlot(str, str)
    def on_info_event(self, message, timestamp):
        """Handle info events"""
        self.event_list.addItem(f"[INFO] {timestamp} - {message}")
        self.event_list.item(self.event_list.count() - 1).setForeground(Qt.GlobalColor.blue)
    
    @pyqtSlot(str, str, int)
    def on_warning_event(self, message, timestamp, priority):
        """Handle warning events"""
        self.event_list.addItem(f"[WARNING] {timestamp} - {message} (Priority: {priority})")
        self.event_list.item(self.event_list.count() - 1).setForeground(Qt.GlobalColor.darkYellow)
    
    @pyqtSlot(str, str, int, str)
    def on_error_event(self, message, timestamp, code, source):
        """Handle error events"""
        self.event_list.addItem(f"[ERROR] {timestamp} - {message} (Code: {code}, Source: {source})")
        self.event_list.item(self.event_list.count() - 1).setForeground(Qt.GlobalColor.red)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Notifier - Signal/Slot")
        self.setGeometry(100, 100, 500, 400)
        
        # Set central widget
        self.event_monitor = EventMonitor()
        self.setCentralWidget(self.event_monitor)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()