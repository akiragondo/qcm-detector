from PyQt5 import QtWidgets,QtCore
from rtqcm.controllers.view_controller import ViewController
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
    display_monitor = 1
    monitor = QtWidgets.QDesktopWidget().screenGeometry(display_monitor)
    main_window.move(monitor.left(),monitor.top())
    sys.exit(app.exec_())