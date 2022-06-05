import cv2
from PyQt6.QtWidgets import QApplication
import hypercube
import paths
import qt_utilities
import sys
from window import Window

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    hc = hypercube.Hypercube(paths.HYPERSPECTRAL_SAMPLE)
    start_index = (15, 5)
    chunk_size = 128
    i, j = 0, 0
    hc.save_chunks('', chunk_size, cv2.imread('C:/Users/alr00/Downloads/Test.png', cv2.IMREAD_COLOR))
    #band = hc.band_to_cv_image(100)
    #band = hc.calculate_ndvi(threshold=0.4)

    #cv2.imshow("image", band)
    #cv2.waitKey()

    app = QApplication([])

    window = Window()
    window.show()

    # Start the event loop.
    app.exec()
