from PyQt5 import QtWidgets,QtCore
from rtqcm.controllers.ViewController import ViewController
import sys

def run_app():
    """
    Top-level function for executing the App
    """
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    mainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    ui = ViewController(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())