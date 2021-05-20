from PyQt5.QtCore import (
    QThread,
)
from PyQt5.QtWidgets import (
    QFileDialog,
)
import pyqtgraph as pg
from rtqcm.utils.main_window_template import MainWindowTemplate
from rtqcm.controllers.run_controller import RunController
from rtqcm.models.connection_parameters import ConnectionParameters
from rtqcm.models.detection import Detection
from rtqcm.api.ports import list_serial_ports
import datetime
from rtqcm.utils.file import (
    get_simulation_filename_from_name,
    get_dir_from_name
)
from rtqcm.utils.interface_utils import colors

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
        self.simulationToggle.toggled.connect(
            self.toggle_simulation_port)
        self.searchButton.clicked.connect(self.search_output_directory)
        self.emailTestButton.clicked.connect(self.verify_email)

        # Run Controller Connections
        self.thread = QThread()
        self.rc = RunController()
        # Run Controller worker thread setup
        self.rc.plot_data.connect(self.update_plot)
        self.rc.detection.connect(self.handle_detection)
        self.rc.finished.connect(self.thread.deleteLater)
        self.rc.disconnect_timeout.connect(self.handle_timeout)
        self.rc.moveToThread(self.thread)
        self.thread.start()

        # DEBUG ONLY
        self.dataFileField.setText('/home/kimino/soft/qcm-detector/data/output/21-01-11_long-calibration-arima'
                                   '-overnight-CrAu_1-data.csv')
        self.outputField.setText('/home/kimino/soft/qcm-detector/data/')
        self.fileName.setText('test.csv')

        # Set up graph variables
        # update viewbox
        self.update_views()
        self.plotLine.getViewBox().sigResized.connect(self.update_views)

        self.vlines = []
        self.events = []
        self.clear_graph_elements()
        self.last_timestamp = None

    def handle_timeout(self):
        self.resultsLabel.setText(
            f'Connection timed out')
        self.disconnect()

    def handle_detection(self, detection : Detection):
        self.add_detection_event(
            time=detection.timestamp,
            severity=detection.severity
        )
        self.add_vline(
            x=detection.timestamp,
            color=colors[detection.severity]
        )
        #Handle emails and vlines

    def connect(self):
        # Connect to the main run controller
        connection_successful = False
        connection_params = ConnectionParameters(
            port_name=self.portComboBox.currentText(),
            gate_time=1000,
            scale_factor=200,
            simulation_data_path=self.dataFileField.text()
        )
        if not self.is_simulated:
            connection_successful = self.rc.start_run(connection_params=connection_params)
        else:
            connection_successful = self.rc.start_simulated_run(connection_params=connection_params)
        if connection_successful:
            self.is_connected = True
            self.disable_main_elements()
        else:
            self.is_connected = False
            self.resultsLabel.setText('Connection unsuccessful')

    def add_initial_connection_event(self, time):
        self.add_past_event(time, 'Connection Started', colors['system'])

    def add_disconnection_event(self, time):
        self.add_past_event(time, 'System Disconnected', colors['system'])

    def add_detection_event(self, time, severity):
        if severity > 0:
            self.add_past_event(time, 'Possible Contamination Detected', colors['mild'])
        else:
            self.add_past_event(time, 'Severe Contamination Detected', colors['severe'])

    def disconnect(self):
        # Handle disconnecting from the main run controller
        self.rc.stop_run()
        self.is_connected = False
        self.enable_main_elements()
        if self.last_timestamp is not None:
            self.add_disconnection_event(self.last_timestamp)
            self.last_timestamp = None

    def connect_button_handler(self):
        # placeholder
        if self.is_connected:
            self.disconnect()
        else:
            self.connect()
            self.clear_graph_elements()

    def clear_graph_elements(self):
        self.update_plot([[],[],[]])
        self.plotLine.clear()
        self.twinLine.clear()
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

    def toggle_simulation_port(self, is_simulated):
        if is_simulated:
            self.is_simulated = is_simulated
            self.connectionTypeLabel.setText('Simulation File')
            self.refreshButton.setText('Search')
            self.refreshButton.clicked.disconnect()
            self.refreshButton.clicked.connect(self.search_simulation_file)
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.is_simulated = is_simulated
            self.connectionTypeLabel.setText('Connection Port')
            self.refreshButton.setText('Refresh')
            self.refreshButton.clicked.disconnect()
            self.refreshButton.clicked.connect(self.refresh_ports_combo)
            self.stackedWidget.setCurrentIndex(0)

    def add_vline(self, x, color):
        new_line = pg.InfiniteLine(pos=x, pen=pg.mkPen(color=color, width=2))
        self.vlines.append(new_line)
        self.plotLine.getViewBox().addItem(new_line)

    def clear_vlines(self):
        for vline in self.vlines:
            self.plotLine.getViewBox().removeItem(vline)

    def add_past_event(self, time, description, color):
        time_text = datetime.datetime.fromtimestamp(time).strftime("%H:%M - %d/%m/%Y")
        content = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; " \
                  "-qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\',\'sans-serif\'; " \
                  "font-size:14px; color:{};\">•</span><span style=\"font-family:\'arial\',\'sans-serif\'; " \
                  "font-size:14px; color:#f3f6f5;\"> {} - {}</span></p></td></tr></table>\n".format(color,
                                                                                                    time_text,
                                                                                                    description)
        content = content + self.textBrowser.toHtml()
        self.textBrowser.setText(content)

    def search_simulation_file(self):
        filename = str(QFileDialog.getOpenFileName(
            self.window, "Select Simulator File")[0])
        self.dataFileField.setText(
            filename
        )
        self.outputField.setText(
            get_dir_from_name(filename)
        )
        self.fileName.setText(
            get_simulation_filename_from_name(filename)
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

    def handle_initial_data(self, data):
        if len(data[0]) > 0:
            if self.last_timestamp is None:
                self.last_timestamp = data[0][-1]
                self.add_initial_connection_event(self.last_timestamp)

    def update_plot(self, data):
        """
        Data: two stacked np arrays
        """
        self.handle_initial_data(data)
        self.plotLine.setData(data[0], data[2])
        self.twinLine.setData(data[0], data[1])

    def update_views(self):
        self.twinGraph.setGeometry(
            self.plotLine.getViewBox().sceneBoundingRect())
        self.twinGraph.linkedViewChanged(
            self.plotLine.getViewBox(), self.twinGraph.XAxis)
