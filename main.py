import cv2
from PyQt6.QtWidgets import QApplication
import hypercube
import paths
import sys
from window import Window

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    hc = hypercube.Hypercube(paths.HYPERSPECTRAL_SAMPLE)
    band = hc.band_to_cv_image(0)
    hc.calculate_NDVI()

    cv2.imshow("image", band)
    cv2.waitKey()

    app = QApplication([])

    window = Window()
    window.show()

    # Start the event loop.
    app.exec()
