from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from algo import *

qtCreatorFile = "interface.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Interface(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
