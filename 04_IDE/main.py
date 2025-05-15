import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, 
                           QWidget, QToolBar, QStatusBar, QFileDialog, 
                           QMessageBox, QSplitter, QPlainTextEdit)
from PyQt6.QtGui import QAction, QFont, QKeySequence, QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt6.QtCore import Qt, QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def", "del",
            "elif", "else", "except", "False", "finally", "for", "from", "global",
            "if", "import", "in", "is", "lambda", "None", "nonlocal", "not", "or",
            "pass", "raise", "return", "True", "try", "while", "with", "yield"
        ]
        for word in keywords:
            pattern = QRegularExpression(r'\b' + word + r'\b')
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Functions
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DCDCAA"))
        pattern = QRegularExpression(r'\b[A-Za-z0-9_]+(?=\()')
        self.highlighting_rules.append((pattern, function_format))
        
        # String literals
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        pattern = QRegularExpression(r'".*?"')
        self.highlighting_rules.append((pattern, string_format))
        pattern = QRegularExpression(r"'.*?'")
        self.highlighting_rules.append((pattern, string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        pattern = QRegularExpression(r'#.*$')
        self.highlighting_rules.append((pattern, comment_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))
        pattern = QRegularExpression(r'\b\d+\b')
        self.highlighting_rules.append((pattern, number_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set monospace font for code
        font = QFont("Courier New", 10)
        self.setFont(font)
        
        # Set tab width
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))
        
        # Apply syntax highlighter
        self.highlighter = PythonHighlighter(self.document())


class SimpleIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Simple IDE")
        self.setGeometry(100, 100, 1000, 600)
        
        # Create splitter for editor and output
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Create code editor
        self.editor = CodeEditor()
        splitter.addWidget(self.editor)
        
        # Create output console
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFont(QFont("Courier New", 10))
        self.output_console.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.output_console.setMinimumHeight(100)
        splitter.addWidget(self.output_console)
        
        # Set splitter sizes (70% editor, 30% output)
        splitter.setSizes([700, 300])
        
        # Set central widget
        self.setCentralWidget(splitter)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create menu
        self.create_menu()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def create_menu(self):
        # Create menu bar
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # New file action
        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        # Open file action
        open_action = QAction("&Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Save file action
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # Save As file action
        saveas_action = QAction("Save &As", self)
        saveas_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        saveas_action.triggered.connect(self.save_file_as)
        file_menu.addAction(saveas_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        # Undo action
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        # Redo action
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Cut action
        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)
        
        # Copy action
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)
        
        # Paste action
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)
        
        # Run menu
        run_menu = menubar.addMenu("&Run")
        
        # Run action
        run_action = QAction("&Run", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)

    def create_toolbar(self):
        # Create toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # New file action
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)
        
        # Open file action
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        # Save file action
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Run action
        run_action = QAction("Run", self)
        run_action.triggered.connect(self.run_code)
        toolbar.addAction(run_action)

    def new_file(self):
        if self.maybe_save():
            self.editor.clear()
            self.current_file = None
            self.setWindowTitle("Simple IDE - [New File]")
            self.statusBar.showMessage("New file created")

    def open_file(self):
        if self.maybe_save():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Open File", "", "Python Files (*.py);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'r') as f:
                        self.editor.setPlainText(f.read())
                    self.current_file = file_path
                    self.setWindowTitle(f"Simple IDE - {os.path.basename(file_path)}")
                    self.statusBar.showMessage(f"Opened {file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")

    def save_file(self):
        if self.current_file:
            return self.save_to_file(self.current_file)
        return self.save_file_as()

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "Python Files (*.py);;All Files (*)"
        )
        if file_path:
            return self.save_to_file(file_path)
        return False

    def save_to_file(self, file_path):
        try:
            with open(file_path, 'w') as f:
                f.write(self.editor.toPlainText())
            self.current_file = file_path
            self.setWindowTitle(f"Simple IDE - {os.path.basename(file_path)}")
            self.statusBar.showMessage(f"Saved to {file_path}")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
            return False

    def maybe_save(self):
        if not self.editor.document().isModified():
            return True
        
        reply = QMessageBox.question(
            self, "Save Changes?",
            "The document has been modified. Save changes?",
            QMessageBox.StandardButton.Save | 
            QMessageBox.StandardButton.Discard | 
            QMessageBox.StandardButton.Cancel
        )
        
        if reply == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif reply == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def run_code(self):
        if self.current_file is None:
            if not self.save_file():
                return
        else:
            self.save_file()
        
        self.output_console.clear()
        self.output_console.append(f"Running: {self.current_file}\n")
        
        try:
            # Run the Python script and capture output
            result = subprocess.run(
                [sys.executable, self.current_file],
                capture_output=True,
                text=True
            )
            
            # Display stdout
            if result.stdout:
                self.output_console.append("--- Output ---\n")
                self.output_console.append(result.stdout)
            
            # Display stderr
            if result.stderr:
                self.output_console.append("--- Errors ---\n")
                self.output_console.append(result.stderr)
                
            # Show exit code
            self.output_console.append(f"\n--- Process completed with exit code {result.returncode} ---")
            
        except Exception as e:
            self.output_console.append(f"Error executing script: {str(e)}")

    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    # Set dark theme
    app.setStyle("Fusion")
    ide = SimpleIDE()
    ide.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()