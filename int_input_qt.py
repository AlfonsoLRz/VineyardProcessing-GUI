from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


# A simple widget consisting of a QLabel and a QLineEdit that
# uses a QIntValidator to ensure that only integer inputs are
# accepted. This class could be implemented in a separate
# script called, say, labelled_int_field.py
class LabelledIntField(QWidget):
    def __init__(self, title, initial_value=None, width=80):
        QWidget.__init__(self)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel()
        self.label.setText(title)
        self.label.setFixedWidth(100)
        layout.addWidget(self.label)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFixedWidth(width)
        self.lineEdit.setValidator(QIntValidator())

        if initial_value != None:
            self.lineEdit.setText(str(initial_value))

        layout.addWidget(self.lineEdit)
        layout.addStretch()

    def set_label_width(self, width):
        self.label.setFixedWidth(width)

    def set_input_width(self, width):
        self.lineEdit.setFixedWidth(width)

    def get_change_signal(self):
        return self.lineEdit.textChanged

    def get_value(self):
        return int(self.lineEdit.text())