from PyQt5 import QtWidgets
from rtqcm.controllers.ViewController import ViewController
import sys

def run_app():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = ViewController(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())