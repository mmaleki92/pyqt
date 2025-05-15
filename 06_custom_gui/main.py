import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QRect


class CustomButton(QWidget):
    def __init__(self, text="Click Me"):
        super().__init__()
        self.text = text
        self.is_pressed = False
        self.is_hover = False
        
        # Enable mouse tracking for hover effect
        self.setMouseTracking(True)
        
        # Fixed size for the button
        self.setMinimumSize(120, 40)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Define the button rectangle
        rect = QRect(0, 0, self.width(), self.height())
        
        # Choose colors based on button state
        if self.is_pressed:
            # Pressed state - darker color
            bg_color = QColor(70, 130, 180)  # Steel Blue
        elif self.is_hover:
            # Hover state - brighter color
            bg_color = QColor(100, 180, 220)  # Light blue
        else:
            # Normal state
            bg_color = QColor(80, 150, 200)  # Medium blue
        
        # Draw button background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(rect, 10, 10)
        
        # Draw text
        painter.setPen(QPen(QColor(255, 255, 255)))
        font = painter.font()
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_pressed = True
            self.update()  # Trigger repaint
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_pressed = False
            self.update()  # Trigger repaint
            # Emit signal or perform action here when clicked
            print("Button clicked!")
    
    def enterEvent(self, event):
        self.is_hover = True
        self.update()  # Trigger repaint
    
    def leaveEvent(self, event):
        self.is_hover = False
        self.is_pressed = False
        self.update()  # Trigger repaint


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Painted Button")
        self.setGeometry(100, 100, 300, 200)
        
        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Add custom button to layout
        self.custom_button = CustomButton("Click Me!")
        layout.addWidget(self.custom_button)
        
        # Set central widget
        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()