import cv2
import hsi_database
import int_input_qt
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import qt_line
from PyQt6.QtWidgets import *
import qt_utilities


class SaveTabWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._hsi_database = hsi_database.HSIDatabase()
        self._filename = ''
        self._save_dir = 'D:\\Github\\InteractiveVineyardClassification\\Datasets\\'

        self._main_layout = QHBoxLayout(self)
        self._main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._main_layout)

        # First panel
        self._layout_v1 = QVBoxLayout(self)
        self._layout_v1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout_v1.setContentsMargins(20, 20, 20, 20)
        self._main_layout.addLayout(self._layout_v1, stretch=1)

        # Save cube into chunks
        self._open_button = QPushButton("Save Hyperspectral Chunks", self)
        self._open_button.setFixedWidth(250)
        self._open_button.clicked.connect(self._save_hsi_chunks)
        self._layout_v1.addWidget(self._open_button)

        self._save_message = QLabel(self)
        self._layout_v1.addWidget(self._save_message)

        self._layout_save_whole_cube = QVBoxLayout(self)
        self._layout_save_whole_cube.setContentsMargins(0, 10, 0, 0)
        self._layout_save_whole_cube.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout_v1.addLayout(self._layout_save_whole_cube)

        self._save_whole_button = QPushButton("Save Whole Hyperspectral Cube", self)
        self._save_whole_button.setFixedWidth(250)
        self._save_whole_button.clicked.connect(self._save_whole_hsi_cube)
        self._layout_save_whole_cube.addWidget(self._save_whole_button)

        self._save_message_whole = QLabel(self)
        self._layout_save_whole_cube.addWidget(self._save_message_whole)

        self._layout_v1.addWidget(qt_line.QHLine())

        self._layout_options = QVBoxLayout(self)
        self._layout_options.setContentsMargins(0, 10, 0, 0)
        self._layout_options.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout_v1.addLayout(self._layout_options)

        self._nparray_checkbox = QCheckBox(self, text='Save as binary numpy array')
        self._layout_options.addWidget(self._nparray_checkbox)

        self._int_value_selector = int_input_qt.LabelledIntField("Subdivision Size", initial_value=128, width=100)
        self._layout_options.addWidget(self._int_value_selector)

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

    def resizeEvent(self, a0: QResizeEvent) -> None:
        print('')
        #if self._qt_image is not None:
        #    self._image_label.setPixmap(qt_utilities.rescale_qt_image(self._qt_image, self.width(), self.height()))

    def _save_hsi_chunks(self):
        self._filename = QFileDialog.getExistingDirectory(self, 'Select Directory', directory=self._save_dir,)

        if self._filename:
            self._save_message.setText('Directory: ' + self._filename)
            self._filename += '/'
            self._save_dir = self._filename
        else:
            self._save_message.setText('')
            return

        self._hsi_database.save_hsi_chunks(self._filename, self._int_value_selector.get_value(),
                                           as_nparray=self._nparray_checkbox.isChecked())

    def _save_whole_hsi_cube(self):
        self._filename = QFileDialog.getExistingDirectory(self, 'Select Directory', directory=self._save_dir)

        if self._filename:
            self._save_message_whole.setText('Directory: ' + self._filename)
            self._filename += '/'
            self._save_dir = self._filename
        else:
            self._save_message_whole.setText('')
            return

        self._hsi_database.save_whole_hsi_cube(self._filename)
