from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QTextEdit, QWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interactive Classification")
        self.setMinimumSize(QSize(400, 300))

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)

        for n, color in enumerate(["red", "green", "blue", "yellow"]):
            tabs.addTab(QWidget(), "Hola")

        self.setCentralWidget(tabs)
