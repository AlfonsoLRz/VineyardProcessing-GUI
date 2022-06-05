import cv2
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


def opencv_to_qt(cv_image):
    h, w, ch = cv_image.shape
    bytes_per_line = ch * w

    return QPixmap.fromImage(QImage(cv_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888))


def rescale_qt_image(qt_image, width, height):
    img = qt_image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
    return img