import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableView, QWidget,
                           QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
                           QLabel, QHeaderView, QMessageBox, QDialog, QFormLayout,
                           QDialogButtonBox, QComboBox, QSpinBox)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSortFilterProxyModel, pyqtSlot
from PyQt6.QtGui import QColor


class Student:
    def __init__(self, id=0, name="", age=0, grade="", major=""):
        self.id = id
        self.name = name
        self.age = age
        self.grade = grade
        self.major = major


class StudentTableModel(QAbstractTableModel):
    """Custom data model for student records"""
    
    def __init__(self):
        super().__init__()
        self.students = []
        self.headers = ["ID", "Name", "Age", "Grade", "Major"]
        
        # Add some example data
        self.add_student(Student(1, "Alice Smith", 20, "A", "Computer Science"))
        self.add_student(Student(2, "Bob Johnson", 19, "B", "Mathematics"))
        self.add_student(Student(3, "Carol White", 21, "A-", "Physics"))
        self.add_student(Student(4, "David Brown", 20, "C+", "Chemistry"))
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.students)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
            
        if role == Qt.ItemDataRole.DisplayRole:
            student = self.students[index.row()]
            col = index.column()
            
            if col == 0:
                return student.id
            elif col == 1:
                return student.name
            elif col == 2:
                return student.age
            elif col == 3:
                return student.grade
            elif col == 4:
                return student.major
        
        elif role == Qt.ItemDataRole.BackgroundRole:
            student = self.students[index.row()]
            # Highlight students with A grades
            if index.column() == 3 and student.grade.startswith('A'):
                return QColor(220, 255, 220)  # Light green
        
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return None
    
    def add_student(self, student):
        # Insert at the end of the list
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.students.append(student)
        self.endInsertRows()
        return True
    
    def remove_student(self, row):
        if row < 0 or row >= self.rowCount():
            return False
            
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.students[row]
        self.endRemoveRows()
        return True
    
    def update_student(self, row, student):
        if row < 0 or row >= self.rowCount():
            return False
            
        self.students[row] = student
        # Emit signal that the data has changed
        self.dataChanged.emit(self.index(row, 0), self.index(row, self.columnCount() - 1))
        return True


class StudentDialog(QDialog):
    """Dialog for adding or editing student records"""
    
    def __init__(self, student=None, parent=None):
        super().__init__(parent)
        self.student = student
        self.setWindowTitle("Add Student" if student is None else "Edit Student")
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        
        # ID field
        self.id_field = QSpinBox()
        self.id_field.setRange(1, 9999)
        layout.addRow("ID:", self.id_field)
        
        # Name field
        self.name_field = QLineEdit()
        layout.addRow("Name:", self.name_field)
        
        # Age field
        self.age_field = QSpinBox()
        self.age_field.setRange(16, 99)
        layout.addRow("Age:", self.age_field)
        
        # Grade field
        self.grade_field = QComboBox()
        for grade in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]:
            self.grade_field.addItem(grade)
        layout.addRow("Grade:", self.grade_field)
        
        # Major field
        self.major_field = QLineEdit()
        layout.addRow("Major:", self.major_field)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                     QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)
        
        # Fill fields if editing
        if self.student:
            self.id_field.setValue(self.student.id)
            self.name_field.setText(self.student.name)
            self.age_field.setValue(self.student.age)
            index = self.grade_field.findText(self.student.grade)
            if index >= 0:
                self.grade_field.setCurrentIndex(index)
            self.major_field.setText(self.student.major)
    
    def get_student(self):
        return Student(
            id=self.id_field.value(),
            name=self.name_field.text(),
            age=self.age_field.value(),
            grade=self.grade_field.currentText(),
            major=self.major_field.text()
        )


class StudentRecordsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Records - MVC Pattern Example")
        self.setGeometry(100, 100, 800, 500)
        
        self.init_ui()
    
    def init_ui(self):
        # Create central widget and layouts
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Create the model
        self.model = StudentTableModel()
        
        # Create a proxy model for sorting and filtering
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        
        # Search box
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Filter by name or major")
        self.search_field.textChanged.connect(self.filter_records)
        search_layout.addWidget(self.search_field)
        main_layout.addLayout(search_layout)
        
        # Table view
        self.table_view = QTableView()
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.table_view)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Student")
        self.add_button.clicked.connect(self.add_student)
        button_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("Edit Student")
        self.edit_button.clicked.connect(self.edit_student)
        button_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Delete Student")
        self.delete_button.clicked.connect(self.delete_student)
        button_layout.addWidget(self.delete_button)
        
        main_layout.addLayout(button_layout)
        
        # Set central widget
        self.setCentralWidget(central_widget)
    
    @pyqtSlot()
    def add_student(self):
        dialog = StudentDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_student = dialog.get_student()
            self.model.add_student(new_student)
    
    @pyqtSlot()
    def edit_student(self):
        indexes = self.table_view.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, "No Selection", "Please select a student to edit.")
            return
            
        # Get the row in the proxy model
        proxy_row = indexes[0].row()
        
        # Convert to source model row
        source_row = self.proxy_model.mapToSource(self.proxy_model.index(proxy_row, 0)).row()
        
        student = self.model.students[source_row]
        dialog = StudentDialog(student, self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_student = dialog.get_student()
            self.model.update_student(source_row, updated_student)
    
    @pyqtSlot()
    def delete_student(self):
        indexes = self.table_view.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, "No Selection", "Please select a student to delete.")
            return
            
        # Get the row in the proxy model
        proxy_row = indexes[0].row()
        
        # Convert to source model row
        source_row = self.proxy_model.mapToSource(self.proxy_model.index(proxy_row, 0)).row()
        
        # Confirm deletion
        student = self.model.students[source_row]
        reply = QMessageBox.question(self, "Confirm Deletion",
                                   f"Are you sure you want to delete {student.name}?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.model.remove_student(source_row)
    
    @pyqtSlot(str)
    def filter_records(self, text):
        self.proxy_model.setFilterKeyColumn(-1)  # Filter all columns
        self.proxy_model.setFilterFixedString(text)


def main():
    app = QApplication(sys.argv)
    window = StudentRecordsApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()