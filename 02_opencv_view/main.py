import sys
import cv2
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, 
                           QVBoxLayout, QWidget, QPushButton, QHBoxLayout,
                           QFileDialog, QMessageBox)

class OpenCVImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_image = None

    def init_ui(self):
        # Set window properties
        self.setWindowTitle('OpenCV Image Viewer with PyQt6')
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create toolbar
        toolbar = QHBoxLayout()
        
        # Open image button
        self.open_button = QPushButton("Open Image")
        self.open_button.clicked.connect(self.open_image)
        toolbar.addWidget(self.open_button)
        
        # Grayscale conversion button
        self.gray_button = QPushButton("Convert to Grayscale")
        self.gray_button.clicked.connect(self.convert_to_gray)
        toolbar.addWidget(self.gray_button)
        
        # Edge detection button
        self.edge_button = QPushButton("Detect Edges")
        self.edge_button.clicked.connect(self.detect_edges)
        toolbar.addWidget(self.edge_button)
        
        # Reset button
        self.reset_button = QPushButton("Reset Image")
        self.reset_button.clicked.connect(self.reset_image)
        toolbar.addWidget(self.reset_button)
        
        # Add toolbar to main layout
        layout.addLayout(toolbar)
        
        # Create image display area
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("Open an image to get started")
        layout.addWidget(self.image_label)
        
        # Store the original image
        self.original_image = None

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        
        if file_path:
            try:
                # Load image with OpenCV
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    raise ValueError("Failed to load image")
                
                # Make a copy for current display
                self.current_image = self.original_image.copy()
                
                # Display the image
                self.display_cv_image(self.current_image)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open image: {str(e)}")

    def convert_to_gray(self):
        if self.current_image is not None:
            # Convert the image to grayscale
            self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            
            # Convert back to 3 channels for display consistency
            if len(self.current_image.shape) == 2:
                self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_GRAY2BGR)
                
            self.display_cv_image(self.current_image)

    def detect_edges(self):
        if self.current_image is not None:
            # Convert to grayscale if not already
            if len(self.current_image.shape) == 3:
                gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            else:
                gray = self.current_image.copy()
            
            # Apply Canny edge detector
            edges = cv2.Canny(gray, 50, 150)
            
            # Convert back to BGR for display
            self.current_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.display_cv_image(self.current_image)

    def reset_image(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.display_cv_image(self.current_image)

    def display_cv_image(self, cv_img):
        """Convert an OpenCV image to QPixmap and display it"""
        if cv_img is None:
            return
        
        # Convert BGR (OpenCV format) to RGB
        if len(cv_img.shape) == 3:
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            
            # Create QImage from the RGB data
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        else:
            # Handle grayscale images
            h, w = cv_img.shape
            bytes_per_line = w
            q_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format.Format_Grayscale8)
        
        # Create QPixmap from QImage and display it
        pixmap = QPixmap.fromImage(q_img)
        
        # Resize pixmap to fit in the label while maintaining aspect ratio
        pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), 
                              Qt.AspectRatioMode.KeepAspectRatio)
        
        self.image_label.setPixmap(pixmap)

    def resizeEvent(self, event):
        """Handle window resize events to resize the displayed image"""
        super().resizeEvent(event)
        if self.current_image is not None:
            self.display_cv_image(self.current_image)

def main():
    app = QApplication(sys.argv)
    viewer = OpenCVImageViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()