import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QGridLayout, QPushButton, QLineEdit)
from PyQt6.QtCore import Qt

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.reset_calc()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Simple Calculator')
        self.setGeometry(300, 300, 300, 400)
        
        # Create central widget and layouts
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setStyleSheet("font-size: 20px; padding: 5px;")
        main_layout.addWidget(self.display)
        
        # Create button grid
        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)
        
        # Button texts and positions
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0, 1, 4)  # Spans all 4 columns
        ]
        
        # Create and add buttons to grid
        for btn_text, row, col, *span in buttons:
            button = QPushButton(btn_text)
            button.setFixedHeight(50)
            button.setStyleSheet("font-size: 16px;")
            
            # Connect button signals to slots
            if btn_text == '=':
                button.clicked.connect(self.calculate_result)
            elif btn_text == 'C':
                button.clicked.connect(self.clear_display)
            else:
                button.clicked.connect(lambda checked, text=btn_text: self.add_to_display(text))
            
            # Set row span and column span if specified
            row_span = span[0] if span else 1
            col_span = span[1] if len(span) > 1 else 1
            grid_layout.addWidget(button, row, col, row_span, col_span)

    def add_to_display(self, text):
        if self.reset_next:
            self.display.clear()
            self.reset_next = False
            
        current = self.display.text()
        self.display.setText(current + text)
    
    def clear_display(self):
        self.display.clear()
        self.reset_calc()
    
    def calculate_result(self):
        try:
            expression = self.display.text()
            result = eval(expression)
            self.display.setText(str(result))
            self.reset_next = True
        except Exception as e:
            self.display.setText("Error")
            self.reset_next = True
    
    def reset_calc(self):
        self.reset_next = False

def main():
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()