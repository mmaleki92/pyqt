import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QFileDialog, QComboBox, QLabel)
from PyQt6.QtGui import QPainter, QPixmap, QImage, QColor
from PyQt6.QtCore import Qt

class ImageCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        
        # Initialize variables
        self.original_pixmap = None
        self.current_pixmap = None
        
    def load_image(self, file_path):
        self.original_pixmap = QPixmap(file_path)
        if self.original_pixmap.isNull():
            return False
        
        self.current_pixmap = self.original_pixmap.copy()
        self.update()
        return True
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Clear background
        painter.fillRect(event.rect(), Qt.GlobalColor.white)
        
        if self.current_pixmap:
            # Calculate position to center the image
            x = (self.width() - self.current_pixmap.width()) // 2
            y = (self.height() - self.current_pixmap.height()) // 2
            painter.drawPixmap(x, y, self.current_pixmap)
            
    def apply_filter(self, filter_name):
        if not self.original_pixmap:
            return
            
        # Convert QPixmap to QImage for pixel manipulation
        image = self.original_pixmap.toImage()
        width = image.width()
        height = image.height()
        
        # Create a new image to store the result
        result_image = QImage(width, height, QImage.Format.Format_ARGB32)
        
        if filter_name == "Grayscale":
            for y in range(height):
                for x in range(width):
                    pixel = image.pixel(x, y)
                    color = QColor(pixel)
                    gray = int(0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue())
                    result_image.setPixelColor(x, y, QColor(gray, gray, gray))
                    
        elif filter_name == "Invert":
            for y in range(height):
                for x in range(width):
                    pixel = image.pixel(x, y)
                    color = QColor(pixel)
                    result_image.setPixelColor(x, y, QColor(255 - color.red(), 
                                                         255 - color.green(), 
                                                         255 - color.blue()))
                    
        elif filter_name == "Sepia":
            for y in range(height):
                for x in range(width):
                    pixel = image.pixel(x, y)
                    color = QColor(pixel)
                    r, g, b = color.red(), color.green(), color.blue()
                    
                    # Sepia conversion
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    
                    # Ensure values are within range
                    tr = min(255, tr)
                    tg = min(255, tg)
                    tb = min(255, tb)
                    
                    result_image.setPixelColor(x, y, QColor(tr, tg, tb))
                    
        elif filter_name == "Red Channel":
            for y in range(height):
                for x in range(width):
                    pixel = image.pixel(x, y)
                    color = QColor(pixel)
                    result_image.setPixelColor(x, y, QColor(color.red(), 0, 0))
        
        elif filter_name == "Original":
            result_image = image.copy()
            
        # Update the current pixmap
        self.current_pixmap = QPixmap.fromImage(result_image)
        self.update()
        
    def reset_image(self):
        if self.original_pixmap:
            self.current_pixmap = self.original_pixmap.copy()
            self.update()


class ImageFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Filter Application")
        self.setGeometry(100, 100, 800, 600)
        
        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Canvas
        self.canvas = ImageCanvas()
        main_layout.addWidget(self.canvas)
        
        # Status label
        self.status_label = QLabel("No image loaded. Use 'Load Image' to start.")
        main_layout.addWidget(self.status_label)
        
        # Controls layout
        controls_layout = QHBoxLayout()
        
        # Load image button
        self.load_btn = QPushButton("Load Image")
        self.load_btn.clicked.connect(self.load_image)
        controls_layout.addWidget(self.load_btn)
        
        # Filter selection
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Original", "Grayscale", "Invert", "Sepia", "Red Channel"])
        self.filter_combo.currentTextChanged.connect(self.apply_filter)
        controls_layout.addWidget(self.filter_combo)
        
        # Reset button
        self.reset_btn = QPushButton("Reset Image")
        self.reset_btn.clicked.connect(self.canvas.reset_image)
        controls_layout.addWidget(self.reset_btn)
        
        main_layout.addLayout(controls_layout)
        self.setCentralWidget(main_widget)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", 
                                             "Image Files (*.png *.jpg *.bmp *.jpeg)")
        if file_path:
            if self.canvas.load_image(file_path):
                self.status_label.setText(f"Image loaded: {file_path}")
            else:
                self.status_label.setText("Failed to load image!")

    def apply_filter(self, filter_name):
        self.canvas.apply_filter(filter_name)
        self.status_label.setText(f"Filter applied: {filter_name}")


def main():
    app = QApplication(sys.argv)
    window = ImageFilterApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()