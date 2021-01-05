from PyQt5 import QtWidgets
from interface.mainApp import MainApp


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = MainApp(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())