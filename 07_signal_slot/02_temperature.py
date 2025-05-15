import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLineEdit, QLabel, QComboBox)
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt


class TemperatureConverter(QWidget):
    # Custom signals
    temp_converted = pyqtSignal(float, str)
    conversion_error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create input field and unit selector
        input_layout = QHBoxLayout()
        self.temp_input = QLineEdit()
        self.temp_input.setPlaceholderText("Enter temperature")
        
        self.from_unit = QComboBox()
        self.from_unit.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        
        input_layout.addWidget(self.temp_input)
        input_layout.addWidget(self.from_unit)
        
        # Add to main layout
        layout.addLayout(input_layout)
        
        # Create display for converted values
        self.result_label = QLabel("Converted temperatures will appear here")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14pt; margin: 10px;")
        layout.addWidget(self.result_label)
        
        # Status message for errors
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)
        
        # Connect signals to slots
        self.temp_input.textChanged.connect(self.calculate_conversion)
        self.from_unit.currentIndexChanged.connect(self.calculate_conversion)
        
        # Connect our custom signals to slots
        self.temp_converted.connect(self.display_result)
        self.conversion_error.connect(self.show_error)
        
        self.setLayout(layout)
    
    @pyqtSlot()
    def calculate_conversion(self):
        """Calculate and emit conversion results or error"""
        # Clear any previous error
        self.status_label.clear()
        
        input_text = self.temp_input.text().strip()
        if not input_text:
            self.result_label.setText("Converted temperatures will appear here")
            return
        
        try:
            temp = float(input_text)
            source_unit = self.from_unit.currentText()
            
            # Convert to all units
            if source_unit == "Celsius":
                celsius = temp
                fahrenheit = celsius * 9/5 + 32
                kelvin = celsius + 273.15
            elif source_unit == "Fahrenheit":
                fahrenheit = temp
                celsius = (fahrenheit - 32) * 5/9
                kelvin = celsius + 273.15
            else:  # Kelvin
                kelvin = temp
                celsius = kelvin - 273.15
                fahrenheit = celsius * 9/5 + 32
            
            # Emit signal with the original temperature and unit
            self.temp_converted.emit(temp, source_unit)
            
        except ValueError:
            self.conversion_error.emit("Please enter a valid number")
    
    @pyqtSlot(float, str)
    def display_result(self, temp, source_unit):
        """Display all converted temperatures"""
        if source_unit == "Celsius":
            celsius = temp
            fahrenheit = celsius * 9/5 + 32
            kelvin = celsius + 273.15
        elif source_unit == "Fahrenheit":
            fahrenheit = temp
            celsius = (fahrenheit - 32) * 5/9
            kelvin = celsius + 273.15
        else:  # Kelvin
            kelvin = temp
            celsius = kelvin - 273.15
            fahrenheit = celsius * 9/5 + 32
        
        result = f"Celsius: {celsius:.2f}°C\n"
        result += f"Fahrenheit: {fahrenheit:.2f}°F\n"
        result += f"Kelvin: {kelvin:.2f}K"
        
        self.result_label.setText(result)
    
    @pyqtSlot(str)
    def show_error(self, message):
        """Display error message"""
        self.status_label.setText(message)
        self.result_label.setText("Error")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temperature Converter - Signal/Slot")
        self.setGeometry(100, 100, 400, 200)
        
        # Set central widget
        self.converter = TemperatureConverter()
        self.setCentralWidget(self.converter)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()