import open_tab
import save_tab
import visualization_tab

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QTextEdit, QWidget, QMessageBox


class Window(QMainWindow):
    NUM_TABS = 3
    TAB_TITLE = ['Open', 'Visualize', 'Save']
    WINDOW_SIZE = (900, 500)

    def __init__(self, size=QSize(WINDOW_SIZE[0], WINDOW_SIZE[1])):
        super().__init__()
        self._tabs = [open_tab.OpenTabWidget(self), visualization_tab.VisualizationWidget(self),
                      save_tab.SaveTabWidget(self)]

        self.setWindowTitle("Interactive Classification")
        self.setMinimumSize(size)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)
        tabs.currentChanged.connect(self.on_tab_change)
        tabs.blockSignals(False)

        for tab_idx in range(self.NUM_TABS):
            self._tabs.append(QWidget())
            tabs.addTab(self._tabs[tab_idx], self.TAB_TITLE[tab_idx])

        self.setCentralWidget(tabs)

    def on_tab_change(self, tab_idx):  # changed!
        if tab_idx == 1:
            self._tabs[tab_idx].update()