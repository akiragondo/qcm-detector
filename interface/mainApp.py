from .mainWindow import Ui_MainWindow
from comms.rs232 import list_serial_ports,RS232
import pyqtgraph as pg
from PyQt5 import QtCore,QtWidgets
from utils.utils import DateAxisItem
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class MainApp(Ui_MainWindow):
    def __init__(self,window):
        #UI Setup
        self.setupUi(window)
        self.window = window
        self.state = 0

        #Time configurations
        self.stabilizationTime = 600
        self.visibleTime = 60*30
        self.drawPeriod = 2
        self.detectPeriod = 60
        self.savePeriod = 30

        #update viewbox
        self.updateViews()
        self.plotLine.getViewBox().sigResized.connect(self.updateViews)

        #Interactions - Connections
        self.is_simulated = False
        self.refresh_ports_combo()
        self.refreshButton.clicked.connect(self.refresh_ports_combo)
        self.is_connected = False
        self.connectButton.clicked.connect(self.connectButtonHandler)
        self.connectionTypeComboBox.currentTextChanged.connect(self.toggleSimulatorPort)
        self.searchButton.clicked.connect(self.searchOutputDirectory)

        #QCM Setup
        self.rs = RS232()
        self.index = 0

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updatePlot)


        # date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation = 'bottom')
        # self.graphWidget = PlotWidget(self.verticalLayoutWidget,
        #                               axisItems = {'bottom': date_axis}
        #                               )
        # self.graphWidget.setMouseEnabled(x=False, y=False)
        # self.graphWidget.setBackground(None)
        # self.graphWidget.setObjectName("graphWidget")
        #
        # #First axis setup
        # self.plotLine = self.graphWidget.plot(pen = pg.mkPen(color='#027CA1', width=3))
        # self.graphWidget.showAxis('left')
        # self.graphWidget.setLabel('left', 'Resistance', units="<font>&Omega;</font>",
        #                           color='#027CA1', **{'font-size':'14pt'})
        # self.graphWidget.getAxis('left').enableAutoSIPrefix(False)
        # #Second axis setup
        # self.graphWidget.showAxis('right')
        # self.graphWidget.setLabel('right', 'Frequency', units="<font>Hz</font>",
        #                           color='#FF8811', **{'font-size':'14pt'})
        # # self.graphWidget.getAxis('right').setPen(pg.mkPen(color='#F3F6F5', width=3))
        #
        # self.twinGraph = pg.ViewBox()
        # self.graphWidget.scene().addItem(self.twinGraph)
        # self.graphWidget.getAxis('right').linkToView(self.twinGraph)
        # self.twinGraph.setXLink(self.graphWidget)
        #
        # self.twinLine = pg.PlotCurveItem(pen = pg.mkPen(color='#FF8811',width=3))
        # self.twinGraph.addItem(self.twinLine)


    def searchOutputDirectory(self):
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self.window, "Select Data Output Directory"))
        self.outputField.setText(file)

    def toggleSimulatorPort(self):
        if self.connectionTypeComboBox.currentText() == 'Simulation File':
            self.is_simulated = True
            self.timer.setInterval(1000/60)
            self.refreshButton.setText('Search')
            self.refreshButton.clicked.disconnect()
            self.refreshButton.clicked.connect(self.searchSimulatorFile)
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.is_simulated = False
            self.timer.setInterval(1000)
            self.refreshButton.setText('Refresh')
            self.refreshButton.clicked.disconnect()
            self.refreshButton.clicked.connect(self.refresh_ports_combo)
            self.stackedWidget.setCurrentIndex(0)

    def add_vline(self, x):
        new_line = pg.InfiniteLine(pos=x)
        self.plotLine.getViewBox().addItem(new_line)

    def searchSimulatorFile(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self.window, "Select Simulator File")
        self.dataFileField.setText(str(file[0]))

    def updateViews(self):
        self.twinGraph.setGeometry(self.plotLine.getViewBox().sceneBoundingRect())
        self.twinGraph.linkedViewChanged(self.plotLine.getViewBox(), self.twinGraph.XAxis)

    def updatePlot(self):
        data = self.rs.read_data()
        if data != None:
            print ('Time: {} - Res: {} - Freq - {}'.format(data['Time'], data['Resistance'], data['Frequency']))
            self.index += 1

        if self.index % self.drawPeriod == 0:
            self.plotLine.setData(self.rs.results[:,0], self.rs.results[:,2])
            self.twinLine.setData(self.rs.results[:,0], self.rs.results[:,1])
            #Update X Range
            if (self.rs.results[:,0][-1]- self.rs.results[:,0][0] > self.visibleTime):
                self.plotLine.getViewBox().setXRange(self.rs.results[:,0][-1] - self.visibleTime, self.rs.results[:,0][-1], padding=5)
            if self.index > self.stabilizationTime and self.state == 1:
                sample = self.rs.results[:,1][-self.stabilizationTime:]
                if sample.std() < 1:
                    self.state = 2
                    self.resultsLabel.setText('Ready')
                    self.progressBar.setValue(100)
                    self.add_vline(self.rs.results[:,0][-1])


        if self.index %self.savePeriod == 0:
            self.rs.append_to_csv()


    def toggle_connect(self):
        self.is_connected = not self.is_connected


    def refresh_ports_combo(self):
        ports_list = list_serial_ports()
        self.portComboBox.clear()
        for port in ports_list:
            self.portComboBox.addItem(port)

    def connectButtonHandler(self):
        if self.is_connected:
            self.toggle_connect()
            self.connectButton.setText('Connect')
            self.timer.stop()

            self.rc = RS232()

            #Disconnect
            self.state = 0
            self.progressBar.setValue(0)
            self.resultsLabel.setText('')

            self.portComboBox.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.emailField.setEnabled(self.checkBox.isChecked())
            self.emailTestButton.setEnabled(True)
            self.refreshButton.setEnabled(True)
            self.fileName.setEnabled(True)
        else:
            #Connect
            port = self.portComboBox.currentText()
            gate_time = 1000
            scale_factor = 200
            output_folder = self.outputField.text()
            if output_folder[-1] != '/':
                output_folder += '/'
            self.rs.set_output_file(output_folder,self.fileName.text())
            result = self.rs.establish_connection(
                port_name=port,
                gate_time=gate_time,
                scale_factor=scale_factor,
                is_simulated=self.is_simulated,
                simulation_data_path=self.dataFileField.text()
            )
            if result == 0:
                self.toggle_connect()
                self.state = 1
                #Connected - Waiting Stabilization
                #Stabilised - Training Model
                #Ready
                self.progressBar.setValue(20)
                self.resultsLabel.setText('Connected - Waiting Stabilization')

                self.connectButton.setText('Cancel')
                #Disable all buttons
                self.portComboBox.setEnabled(False)
                self.checkBox.setEnabled(False)
                self.emailField.setEnabled(False)
                self.emailTestButton.setEnabled(False)
                self.refreshButton.setEnabled(False)
                self.fileName.setEnabled(False)
                self.timer.start()



