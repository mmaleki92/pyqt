import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QComboBox, QPushButton, QColorDialog)
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath
from PyQt6.QtCore import Qt, QPoint, QRect
import math

class ShapeCanvas(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(600, 400)
        
        # Drawing attributes
        self.shape_type = "Rectangle"
        self.drawing = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        
        # Styling
        self.pen_color = QColor(0, 0, 0)
        self.brush_color = QColor(255, 255, 255, 0)  # Transparent by default
        
        # List to store all shapes
        self.shapes = []

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.start_point = event.position().toPoint()
            self.end_point = self.start_point
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.drawing:
            self.end_point = event.position().toPoint()
            self.update()  # Trigger a paint event

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            # Save the completed shape
            shape = {
                "type": self.shape_type,
                "start": QPoint(self.start_point),
                "end": QPoint(self.end_point),
                "pen": QPen(self.pen_color, 2, Qt.PenStyle.SolidLine),
                "brush": QBrush(self.brush_color)
            }
            self.shapes.append(shape)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw white background
        painter.fillRect(event.rect(), Qt.GlobalColor.white)
        
        # Draw all saved shapes
        for shape in self.shapes:
            painter.setPen(shape["pen"])
            painter.setBrush(shape["brush"])
            self.draw_shape(painter, shape["type"], shape["start"], shape["end"])
            
        # Draw current shape if drawing
        if self.drawing:
            painter.setPen(QPen(self.pen_color, 2, Qt.PenStyle.SolidLine))
            painter.setBrush(QBrush(self.brush_color))
            self.draw_shape(painter, self.shape_type, self.start_point, self.end_point)

    def draw_shape(self, painter, shape_type, start, end):
        if shape_type == "Rectangle":
            rect = QRect(start, end)
            painter.drawRect(rect)
        elif shape_type == "Ellipse":
            rect = QRect(start, end)
            painter.drawEllipse(rect)
        elif shape_type == "Line":
            painter.drawLine(start, end)
        elif shape_type == "Triangle":
            points = [start, QPoint(start.x(), end.y()), QPoint(end.x(), end.y())]
            path = QPainterPath()
            path.moveTo(points[0])
            path.lineTo(points[1])
            path.lineTo(points[2])
            path.lineTo(points[0])
            painter.drawPath(path)
        elif shape_type == "Star":
            # Draw a simple star shape
            center_x = (start.x() + end.x()) / 2
            center_y = (start.y() + end.y()) / 2
            radius = min(abs(end.x() - start.x()), abs(end.y() - start.y())) / 2
            
            points = []
            for i in range(10):  # 5 points star has 10 vertices (inner and outer)
                angle = 0.8 * i * 3.14159 / 5
                r = radius if i % 2 == 0 else radius / 2.5
                x = center_x + r * math.cos(angle)
                y = center_y + r * math.sin(angle)
                points.append(QPoint(int(x), int(y)))
            
            path = QPainterPath()
            path.moveTo(points[0])
            for point in points[1:]:
                path.lineTo(point)
            path.lineTo(points[0])
            painter.drawPath(path)

    def set_shape(self, shape):
        self.shape_type = shape

    def set_pen_color(self, color):
        self.pen_color = color

    def set_brush_color(self, color):
        self.brush_color = color

    def clear_canvas(self):
        self.shapes.clear()
        self.update()


class ShapeDrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Shape Drawing App")
        self.setGeometry(100, 100, 800, 600)
        
        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Canvas
        self.canvas = ShapeCanvas()
        main_layout.addWidget(self.canvas)
        
        # Controls layout
        controls_layout = QHBoxLayout()
        
        # Shape selection
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Rectangle", "Ellipse", "Line", "Triangle", "Star"])
        self.shape_combo.currentTextChanged.connect(self.change_shape)
        controls_layout.addWidget(self.shape_combo)
        
        # Pen color button
        self.pen_color_btn = QPushButton("Outline Color")
        self.pen_color_btn.clicked.connect(self.change_pen_color)
        controls_layout.addWidget(self.pen_color_btn)
        
        # Fill color button
        self.fill_color_btn = QPushButton("Fill Color")
        self.fill_color_btn.clicked.connect(self.change_fill_color)
        controls_layout.addWidget(self.fill_color_btn)
        
        # Clear button
        self.clear_btn = QPushButton("Clear Canvas")
        self.clear_btn.clicked.connect(self.canvas.clear_canvas)
        controls_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(controls_layout)
        self.setCentralWidget(main_widget)

    def change_shape(self, shape):
        self.canvas.set_shape(shape)

    def change_pen_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_pen_color(color)

    def change_fill_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_brush_color(color)


def main():
    app = QApplication(sys.argv)
    window = ShapeDrawingApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()