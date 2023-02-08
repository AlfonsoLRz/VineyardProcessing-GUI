import cv2

import app_params
import hsi_database
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import qt_utilities


class VisualizationWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._hsi_database = hsi_database.HSIDatabase()
        self._app_params = app_params.ApplicationParameters()

        self._layer_selected = 0
        self._qt_image_orig = None
        self._qt_image_ndvi = None
        self._qt_image_class = None

        self._main_layout = QHBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        # Panel 1
        self._layout_v1 = QHBoxLayout(self)
        self._layout_v1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._layout_v1.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addLayout(self._layout_v1, stretch=2)

        default_image = QPixmap()
        default_image.fill(QColor('darkGray'))
        self._image_label_orig = QLabel(self)
        self._image_label_orig.setPixmap(default_image)
        self._layout_v1.addWidget(self._image_label_orig)

        self._image_label_ndvi = QLabel(self)
        self._image_label_ndvi.setPixmap(default_image)
        self._layout_v1.addWidget(self._image_label_ndvi)

        self._image_label_class = QLabel(self)
        self._image_label_class.setPixmap(default_image)
        self._layout_v1.addWidget(self._image_label_class)

        # Panel 2
        self._layout_v2 = QVBoxLayout(self)
        self._layout_v2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout_v2.setContentsMargins(40, 15, 40, 40)
        self._main_layout.addLayout(self._layout_v2, stretch=1)

        self._selector_label = QLabel()
        self._layout_v2.addWidget(self._selector_label)

        self._layer_selector = QSlider(Qt.Orientation.Horizontal)
        self._layer_selector.valueChanged.connect(self._on_layer_change)
        self._layout_v2.addWidget(self._layer_selector)

        self._threshold_layout = QVBoxLayout(self)
        self._threshold_layout.setContentsMargins(0, 5, 0, 0)
        self._threshold_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout_v2.addLayout(self._threshold_layout)

        self._threshold_label = QLabel()
        self._threshold_selector = QSlider(Qt.Orientation.Horizontal)
        self._threshold_selector.valueChanged.connect(self._on_threshold_change)
        self._threshold_layout.addWidget(self._threshold_label)
        self._threshold_layout.addWidget(self._threshold_selector)

        self._layout_v3 = QVBoxLayout(self)
        self._layout_v3.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout_v3.setContentsMargins(0, 30, 0, 0)
        self._layout_v2.addLayout(self._layout_v3)

        self._export_rgb_button = QPushButton("Export RGB")
        self._export_rgb_button.setFixedWidth(250)
        self._export_rgb_button.clicked.connect(self._export_rgb_file)
        self._layout_v3.addWidget(self._export_rgb_button)

        self._export_ndvi_button = QPushButton("Export NDVI")
        self._export_ndvi_button.setFixedWidth(250)
        self._export_ndvi_button.clicked.connect(self._export_ndvi_file)
        self._layout_v3.addWidget(self._export_ndvi_button)

        self._export_binary_button = QPushButton("Export Binary")
        self._export_binary_button.setFixedWidth(250)
        self._export_binary_button.clicked.connect(self._export_binary_file)
        self._layout_v3.addWidget(self._export_binary_button)

        self.update()
        self._on_layer_change()
        self._on_threshold_change()

    def _export_binary_file(self):
        name = QFileDialog.getSaveFileName(self, 'Save File')
        if name[0] != '':
            hsi_cube = self._hsi_database.get_hsi_data()
            if hsi_cube is not None:
                hsi_cube.export_binary_file(name[0], self._threshold_selector.value() / 100.0)

    def _export_ndvi_file(self):
        name = QFileDialog.getSaveFileName(self, 'Save File')
        if name[0] != '':
            hsi_cube = self._hsi_database.get_hsi_data()
            if hsi_cube is not None:
                hsi_cube.export_ndvi_file(name[0])

    def _export_rgb_file(self):
        name = QFileDialog.getSaveFileName(self, 'Save File')
        if name[0] != '':
            hsi_cube = self._hsi_database.get_hsi_data()
            if hsi_cube is not None:
                hsi_cube.export_rgb_file(name[0])

    def _on_layer_change(self):
        self._selector_label.setText("Layer Selection: " + str(self._layer_selector.value()))
        self._layer_selected = self._layer_selector.value()
        self.__update_image(only_orig=True)

    def _on_threshold_change(self):
        self._app_params._threshold = self._threshold_selector.value() / 100.0
        self._threshold_label.setText("NDVI Thresholding Factor: " + str(self._threshold_selector.value() / 100.0))
        self.__update_image(only_ndvi=True)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if self._qt_image_orig is not None:
            self._image_label_orig.setPixmap(qt_utilities.rescale_qt_image(self._qt_image_orig, self.width(), self.height()))
            self._image_label_ndvi.setPixmap(qt_utilities.rescale_qt_image(self._qt_image_ndvi, self.width(), self.height()))

        if self._qt_image_class is not None:
            self._image_label_class.setPixmap(qt_utilities.rescale_qt_image(self._qt_image_class, self.width(), self.height()))

    def update(self):
        hsi_cube = self._hsi_database.get_hsi_data()
        if hsi_cube is not None:
            self._layer_selector.setMaximum(hsi_cube.num_layers() - 1)
        else:
            self._layer_selector.setMaximum(0)
        self._layer_selector.setMinimum(0)

        self.__update_image()

    def __update_image(self, only_ndvi=False, only_orig=False):
        hc = self._hsi_database.get_hsi_data()
        if hc is not None:
            if not only_orig:
                band = hc.calculate_ndvi(threshold=self._threshold_selector.value() / 100.0)
                self._qt_image_ndvi = qt_utilities.opencv_to_qt(band)

            if not only_ndvi:
                band = hc.band_to_cv_image(self._layer_selector.value())
                self._qt_image_orig = qt_utilities.opencv_to_qt(band)

        class_image = self._hsi_database.get_classification_img()
        if class_image is not None:
            self._qt_image_class = qt_utilities.opencv_to_qt(class_image)

        self.resizeEvent(a0=None)
