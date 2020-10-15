import sys
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QColumnView,
    QDockWidget,
    QFileDialog,
    QFileSystemModel,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QTreeView,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("PyNotepad")
        self.resize(1024, 768)

        self.home_path = QDir.homePath()

        dock = QDockWidget("File Browser", self)

        self.model = QFileSystemModel()
        self.model.setRootPath(self.home_path)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.home_path))
        self.tree.doubleClicked.connect(self.on_tree_clicked)

        dock.setWidget(self.tree)
        dock.setFloating(False)

        self.editor = QPlainTextEdit()
        self.editor.document().setDefaultFont(QFont("monospace"))
        self.setCentralWidget(self.editor)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        self.file_path = None

        self.create_menu()

    def on_tree_clicked(self, index):
        self.close_event()
        index_item = self.model.index(index.row(), 0, index.parent())
        self.file_path = self.model.filePath(index_item)
        self.open(self.file_path)

    def create_menu(self):
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        new_action = QAction("&New document", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_document)
        file_menu.addAction(new_action)

        open_action = QAction("&Open file...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.show_open_dialog)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save)
        file_menu.addAction(save_action)

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def new_document(self):
        self.close_event()
        self.editor.clear()
        self.file_path = None

    def open(self, file_path):
        file_contents = ""
        with open(file_path) as f:
            file_contents = f.read()
            self.editor.setPlainText(file_contents)

    def show_open_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open...")
        if file_path:
            self.open(file_path)
            self.file_path = file_path

    def save(self):
        if self.file_path is None:
            return self.show_save_dialog()
        else:
            with open(self.file_path, "w") as f:
                f.write(self.editor.toPlainText())
            self.editor.document().setModified(False)
            return True

    def show_save_dialog(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save as...")
        if filename:
            self.file_path = filename
            self.save()
            return True
        return False

    def show_about_dialog(self):
        text = """
            <center>
                <h1>PyNotepad</h1><br/>
                <img src=logo.png width=200 height=200>
            </center>
            <p>Version 0.0.1</p>
        """
        QMessageBox.about(self, "About PyNotepad", text)

    def close_event(self):
        if self.editor.document().isModified():
            answer = self.ask_for_confirmation()
            if answer == QMessageBox.Save:
                if not self.save():
                    return
            elif answer == QMessageBox.Cancel:
                return

    def ask_for_confirmation(self):
        answer = QMessageBox.question(
            window,
            "Confirm closing",
            "You have unsaved changes. Are you sure you want to exit?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
        )
        return answer


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
