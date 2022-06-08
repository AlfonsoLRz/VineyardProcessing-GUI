import cv2
from PyQt6.QtWidgets import QApplication
import hypercube
import paths
import qt_utilities
import sys
from window import Window

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication([])

    window = Window()
    window.show()

    # Start the event loop.
    app.exec()
