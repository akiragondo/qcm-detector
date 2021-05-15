from PyQt5.QtCore import (
    pyqtSignal,
    QThread,
)
from PyQt5.QtWidgets import (
    QFileDialog,
)
import pyqtgraph as pg
from rtqcm.controllers.MainWindowTemplate import MainWindowTemplate
from rtqcm.controllers.RunController import RunController
from rtqcm.models.ConnectionParameters import ConnectionParameters
from rtqcm.api.ports import list_serial_ports
import datetime
import os


class ViewController(MainWindowTemplate):
    """
    Class responsible for the Graphical user interface and Graphical user interface commands
        - Variables inputed by the user
        - Current state of the
            * Graph
            * Events
            * Buttons
            * Progress Bar
            * Results label
    """
    def __init__(self, window):
        self.setupUi(window)
        self.window = window

        self.is_simulated = False
        self.is_connected = False

        # Interactions - Connections
        self.refresh_ports_combo()
        self.refreshButton.clicked.connect(self.refresh_ports_combo)
        self.connectButton.clicked.connect(self.connect_button_handler)
        self.connectionTypeComboBox.currentTextChanged.connect(
            self.toggle_simulation_port)
        self.searchButton.clicked.connect(self.search_output_directory)
        self.emailTestButton.clicked.connect(self.verify_email)

        # Run Controller Connections
        self.thread = QThread()
        self.rc = RunController()
        # Run Controller worker thread setup
        self.rc.plot_data.connect(self.update_plot)
        self.rc.finished.connect(self.thread.deleteLater)
        self.rc.moveToThread(self.thread)
        self.thread.start()

        # update viewbox
        self.update_views()
        self.plotLine.getViewBox().sigResized.connect(self.update_views)

    def connect(self):
        # Connect to the main run controller
        connection_successful = False
        connectionParams = ConnectionParameters(
            port_name= self.portComboBox.currentText(),
            gate_time= 1000,
            scale_factor=200,
            simulation_data_path=self.dataFileField.text()
        )
        if not self.is_simulated:
            connection_successful = self.rc.start_run(connectionParams=connectionParams)
        else:
            connection_successful = self.rc.start_simulated_run(connectionParams=connectionParams)
        if connection_successful:
            self.is_connected = True
            self.disable_main_elements()
        else:
            self.is_connected = False
            self.resultsLabel.setText('Connection unsuccessful')

    def disconnect(self):
        # Handle disconnecting from the main run controller
        self.rc.stop_run()
        self.is_connected = False
        self.enable_main_elements()

    def connect_button_handler(self):
        # placeholder
        if self.is_connected:
            self.disconnect()
        else:
            self.connect()

    def clear_graph_elements(self):
        self.plotLine.clear()
        self.movingAverageLine.clear()
        self.twinLine.clear()
        self.freqMovingAverageLine.clear()
        self.clear_vlines()
        self.textBrowser.clear()

    def disable_main_elements(self):
        # Disable all buttons
        self.connectButton.setText('Cancel')
        self.portComboBox.setEnabled(False)
        self.checkBox.setEnabled(False)
        self.emailField.setEnabled(False)
        self.emailTestButton.setEnabled(False)
        self.refreshButton.setEnabled(False)
        self.fileName.setEnabled(False)
        self.dataFileField.setEnabled(False)
        self.outputField.setEnabled(False)
        self.searchButton.setEnabled(False)

    def enable_main_elements(self):
        self.connectButton.setText('Connect')
        self.portComboBox.setEnabled(True)
        self.checkBox.setEnabled(True)
        self.emailField.setEnabled(self.checkBox.isChecked())
        self.emailTestButton.setEnabled(True)
        self.refreshButton.setEnabled(True)
        self.fileName.setEnabled(True)
        self.dataFileField.setEnabled(True)
        self.searchButton.setEnabled(True)
        self.outputField.setEnabled(True)

    def toggle_connect(self):
        self.is_connected = not self.is_connected

    def toggle_simulation_port(self):
        if self.connectionTypeComboBox.currentText() == 'Simulation File':
            self.is_simulated = True
            self.refreshButton.setText('Search')
            self.refreshButton.clicked.disconnect()
            self.refreshButton.clicked.connect(self.search_simulation_file)
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.is_simulated = False
            self.refreshButton.setText('Refresh')
            self.refreshButton.clicked.disconnect()
            self.refreshButton.clicked.connect(self.refresh_ports_combo)
            self.stackedWidget.setCurrentIndex(0)

    def add_vline(self, x, color):
        new_line =  pg.InfiniteLine(pos=x, pen=pg.mkPen(color=color, width=2))
        self.vlines.append(new_line)
        self.plotLine.getViewBox().addItem(new_line)

    def clear_vlines(self):
        for vline in self.vlines:
            self.plotLine.getViewBox().removeItem(vline)

    def addPastEvent(self, time, description, color):
        """
        :param time: time in timestamp from the results
        """
        timeText = datetime.fromtimestamp(time).strftime("%H:%M - %d/%m/%Y")
        content = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; " \
                  "-qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\',\'sans-serif\'; " \
                  "font-size:14px; color:{};\">•</span><span style=\"font-family:\'arial\',\'sans-serif\'; " \
                  "font-size:14px; color:#f3f6f5;\"> {} - {}</span></p></td></tr></table>\n".format(color,
                                                                                                    timeText,
                                                                                                    description)
        content = content + self.textBrowser.toHtml()
        self.textBrowser.setText(content)

    def get_dirname_from_name(self, filename):
        dirname = os.path.dirname(filename)
        return dirname

    def make_simulation_filename_from_name(self, filename):
        separator = '_'
        name = os.path.basename(filename).split(separator)[1:]
        name = separator.join(name)
        separator = '.'
        name = os.path.basename(filename).split(separator)[0] + '_simulation'
        return name

    def search_simulation_file(self):
        filename = str(QFileDialog.getOpenFileName(
            self.window, "Select Simulator File")[0])
        self.dataFileField.setText(
            filename
        )
        self.outputField.setText(
            self.get_dirname_from_name(filename)
        )
        self.fileName.setText(
            self.make_simulation_filename_from_name(filename)
        )

    def search_output_directory(self):
        file = str(QFileDialog.getExistingDirectory(
            self.window, "Select Data Output Directory"))
        self.outputField.setText(file)

    def verify_email(self):
        pass

    def refresh_ports_combo(self):
        ports_list = list_serial_ports()
        self.portComboBox.clear()
        for port in ports_list:
            self.portComboBox.addItem(port)

    def update_plot(self, data):
        """
        Data: two stacked np arrays
        """
        self.plotLine.setData(data[0], data[2])
        self.twinLine.setData(data[0], data[1])

    def update_views(self):
        self.twinGraph.setGeometry(
            self.plotLine.getViewBox().sceneBoundingRect())
        self.twinGraph.linkedViewChanged(
            self.plotLine.getViewBox(), self.twinGraph.XAxis)
