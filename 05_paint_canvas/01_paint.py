import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QSlider, QPushButton, QColorDialog)
from PyQt6.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt6.QtCore import Qt, QPoint

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        
        # Initialize variables
        self.setMouseTracking(True)
        self.last_point = QPoint()
        self.drawing = False
        
        # Initialize drawing parameters
        self.pen_color = QColor(0, 0, 0)
        self.pen_width = 3
        
        # Create a pixmap to draw on
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(Qt.GlobalColor.white)

    def resizeEvent(self, event):
        # Create new pixmap when resizing, preserving the content
        if self.size().width() > 0 and self.size().height() > 0:
            new_pixmap = QPixmap(self.size())
            new_pixmap.fill(Qt.GlobalColor.white)
            
            # Draw old pixmap onto the new one
            painter = QPainter(new_pixmap)
            painter.drawPixmap(0, 0, self.pixmap)
            painter.end()
            
            self.pixmap = new_pixmap

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
            painter = QPainter(self.pixmap)
            pen = QPen(self.pen_color, self.pen_width, Qt.PenStyle.SolidLine, 
                       Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            
            current_point = event.position().toPoint()
            painter.drawLine(self.last_point, current_point)
            self.last_point = current_point
            
            painter.end()
            self.update()  # Trigger a repaint

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)

    def clear(self):
        self.pixmap.fill(Qt.GlobalColor.white)
        self.update()

    def set_pen_color(self, color):
        self.pen_color = color

    def set_pen_width(self, width):
        self.pen_width = width


class BasicPaintApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Basic Paint Application")
        self.setGeometry(100, 100, 800, 600)
        
        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Canvas
        self.canvas = Canvas()
        main_layout.addWidget(self.canvas)
        
        # Controls layout
        controls_layout = QHBoxLayout()
        
        # Pen width control
        controls_layout.addWidget(QLabel("Pen Width:"))
        self.pen_width_slider = QSlider(Qt.Orientation.Horizontal)
        self.pen_width_slider.setRange(1, 20)
        self.pen_width_slider.setValue(3)
        self.pen_width_slider.valueChanged.connect(self.change_pen_width)
        controls_layout.addWidget(self.pen_width_slider)
        
        # Color picker button
        self.color_btn = QPushButton("Change Color")
        self.color_btn.clicked.connect(self.change_pen_color)
        controls_layout.addWidget(self.color_btn)
        
        # Clear canvas button
        self.clear_btn = QPushButton("Clear Canvas")
        self.clear_btn.clicked.connect(self.canvas.clear)
        controls_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(controls_layout)
        self.setCentralWidget(main_widget)

    def change_pen_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_pen_color(color)

    def change_pen_width(self, width):
        self.canvas.set_pen_width(width)


def main():
    app = QApplication(sys.argv)
    window = BasicPaintApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()