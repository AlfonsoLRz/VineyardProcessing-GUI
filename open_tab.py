import hsi_database
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import qt_utilities


class OpenTabWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._hsi_database = hsi_database.HSIDatabase()
        self._hsi_filename = ""
        self._classification_file = ""
        self._qt_image = None
        self._previous_dir = 'D:\\Github\\InteractiveVineyardClassification\\Datasets\\'

        self._main_layout = QHBoxLayout(self)
        self._main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._main_layout)

        # First panel
        self._layout_v1 = QVBoxLayout(self)
        self._layout_v1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout_v1.setContentsMargins(20, 20, 20, 20)
        self._main_layout.addLayout(self._layout_v1, stretch=3)

        self._open_button = QPushButton("Open Hyperspectral Image", self)
        self._open_button.setFixedWidth(250)
        self._open_button.clicked.connect(self._get_hsi_file)
        self._layout_v1.addWidget(self._open_button)

        self._filename_label = QLabel(self)
        self._layout_v1.addWidget(self._filename_label)

        self._load_message = QLabel(self)
        self._layout_v1.addWidget(self._load_message)

        # Get classification file
        self._layout_v2 = QVBoxLayout(self)
        self._layout_v2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout_v2.setContentsMargins(0, 10, 0, 0)
        self._layout_v1.addLayout(self._layout_v2)

        self._open_class_img_button = QPushButton("Open Hyperspectral Classification", self)
        self._open_class_img_button.setFixedWidth(250)
        self._open_class_img_button.clicked.connect(self._get_class_img)
        self._layout_v2.addWidget(self._open_class_img_button)

        self._class_img_label = QLabel(self)
        self._layout_v2.addWidget(self._class_img_label)

        self._load_img_message = QLabel(self)
        self._layout_v2.addWidget(self._load_img_message)

        # Second panel
        self._layout_v2 = QVBoxLayout(self)
        self._layout_v2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._layout_v2.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addLayout(self._layout_v2, stretch=1)

        default_image = QPixmap()
        default_image.fill(QColor('darkGray'))
        self._image_label = QLabel(self)
        self._image_label.setPixmap(default_image)
        self._layout_v2.addWidget(self._image_label)

    def _get_class_img(self):
        self._classification_file = QFileDialog.getOpenFileName(self, 'Open file', self._previous_dir,
                                                                '"Classification files (*.png)"')[0]

        if self._classification_file:
            self._class_img_label.setText('HSI File: ' + self._classification_file)
            self._class_img_label.setStyleSheet("QLabel{font-size: 8pt;}")
            self._previous_dir = self._classification_file[0:self._classification_file.rfind('/')]

            if self._hsi_database.load_classification_img(self._classification_file):
                self._load_img_message.setText('Loaded successfully...')
                self._load_img_message.setStyleSheet("QLabel{font-size: 8pt; color: green;}")
            else:
                self._load_img_message.setText('Could not be loaded...')
                self._load_img_message.setStyleSheet("QLabel{font-size: 8pt; color: red;}")
                self._classification_file = ''

    def _get_hsi_file(self):
        self._hsi_filename = QFileDialog.getOpenFileName(self, 'Open file', self._previous_dir, '"HSI files (*.hdr)"')[0]
        self._hsi_filename = self._hsi_filename.split('.')[0]

        if self._hsi_filename:
            self._filename_label.setText('HSI File: ' + self._hsi_filename)
            self._filename_label.setStyleSheet("QLabel{font-size: 8pt;}")
            self._previous_dir = self._hsi_filename[0:self._hsi_filename.rfind('/')]

            if self._hsi_database.load_hsi_data(self._hsi_filename):
                self._load_message.setText('Loaded successfully...')
                self._load_message.setStyleSheet("QLabel{font-size: 8pt; color: green;}")

                opencv_image = self._hsi_database.get_hsi_data().band_to_cv_image(150)
                self._qt_image = qt_utilities.opencv_to_qt(opencv_image)
                self._image_label.setPixmap(qt_utilities.rescale_qt_image(self._qt_image, self.width(), self.height()))
            else:
                self._load_message.setText('Could not be loaded...')
                self._load_message.setStyleSheet("QLabel{font-size: 8pt; color: red;}")

                self._qt_image = None
                self._hsi_filename = ''

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if self._qt_image is not None:
            self._image_label.setPixmap(qt_utilities.rescale_qt_image(self._qt_image, self.width(), self.height()))

