from PyQt5 import QtWidgets,QtCore
from rtqcm.controllers.ViewController import ViewController
import sys

def run_app():
    """
    Top-level function for executing the App
    """
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_window.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    ui = ViewController(main_window)
    main_window.show()
    sys.exit(app.exec_())