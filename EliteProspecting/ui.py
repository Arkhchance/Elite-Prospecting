#!/usr/bin/python
from PyQt5.QtWidgets import QApplication, QLabel


class new_ui():
    def __init__(self):
        app = QApplication([])
        label = QLabel('Hello World!')
        label.show()
        app.exec_()
