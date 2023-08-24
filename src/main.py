######################### Xnxe9 <3? #########################
#
#   .o88b.  .d88b.  .d8888. .88b  d88.  .d88b.  .d8888.
#  d8P  Y8 .8P  Y8. 88'  YP 88'YbdP`88 .8P  Y8. 88'  YP
#  8P      88    88 `8bo.   88  88  88 88    88 `8bo.
#  8b      88    88   `Y8b. 88  88  88 88    88   `Y8b.
#  Y8b  d8 `8b  d8' db   8D 88  88  88 `8b  d8' db   8D
#   `Y88P'  `Y88P'  `8888Y' YP  YP  YP  `Y88P'  `8888Y'
# 
# ★ StarLab RPL - COSMOS GROUND STATION ★
# Communications and Observation Station for Mission Operations and Surveillance
#
# By Martin Ortiz
# Version 1.0.0
# Date 06.08.2023
#
#############################################################

######################### Xnxe9 <3? #########################
#
#   .o88b.  .d88b.  .d8888. .88b  d88.  .d88b.  .d8888.
#  d8P  Y8 .8P  Y8. 88'  YP 88'YbdP`88 .8P  Y8. 88'  YP
#  8P      88    88 `8bo.   88  88  88 88    88 `8bo.
#  8b      88    88   `Y8b. 88  88  88 88    88   `Y8b.
#  Y8b  d8 `8b  d8' db   8D 88  88  88 `8b  d8' db   8D
#   `Y88P'  `Y88P'  `8888Y' YP  YP  YP  `Y88P'  `8888Y'
#
# ★ StarLab RPL - COSMOS GROUND STATION ★
# Communications and Observation Station for Mission Operations and Surveillance
#
# By Martin Ortiz
# Version 1.0.0
# Date 06.08.2023
#
#############################################################


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QIcon, QKeySequence
from qframelesswindow import FramelessMainWindow

from src.models import PreferenceModel
from src.controllers import (
    WindowController,
    ConnectionController,
    TerminalController,
    RecordingController,
)

from src.ui import Ui_MainWindow, CustomTitleBar


class MainWindow(FramelessMainWindow):
    """MainWindow class"""

    def __init__(self) -> None:
        super().__init__()

        # Set a custom title bar for the window
        self.setTitleBar(CustomTitleBar(self))

        # Setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # load preferences
        self.preferences = PreferenceModel()
        self.window_controller = WindowController(self)
        self.terminal_controller = TerminalController(self)
        self.recording_controller = RecordingController(self)
        self.connection_controller = ConnectionController(self)

        # get the application information
        self.name = self.preferences.get("name")
        self.version = self.preferences.get("version")
        self.dev_phase = self.preferences.get("dev_phase")
        self.author = self.preferences.get("author")

        # set up window properties
        self.setWindowIcon(QIcon(self.preferences.get("icon")))
        self.setWindowTitle(self.name.upper())

        # update the labels that display the info of the application
        self.ui.label_statusBar.setText(
            f"{self.name.lower()}-v{self.version}-{self.dev_phase}"
        )

        # change the current apparence
        self.ui.stackedWidget_central.setCurrentWidget(self.ui.page_centralDashboard)

        self.setup_signals()

        self.titleBar.raise_()
        self.show()

    def setup_signals(self):
        """
        connect all the signas of the components to the controllers
        """
        ## SIGNALS
        self.connection_controller.serial_model.write_to_terminal.connect(
            self.terminal_controller.write
        )

        ## WINDOW CONTROLLER
        shortcut = QShortcut(QKeySequence(Qt.Key_F11), self)
        shortcut.activated.connect(self.window_controller.toggle_fullscreen)

        self.ui.btn_smallModeTogle.clicked.connect(
            self.window_controller.toggle_small_mode
        )
        self.ui.btn_connectionDroDown.clicked.connect(
            self.window_controller.toggle_connection_dropdown
        )
        self.ui.btn_preferencesToggle.clicked.connect(
            self.window_controller.toggle_preferences_page
        )
        self.ui.btn_goBackHome.clicked.connect(
            self.window_controller.toggle_preferences_page
        )

        # RECORDING CONTROLLER
        self.ui.btn_toggleRecordings.clicked.connect(
            self.recording_controller.toggle_recordings
        )
        self.ui.btn_toggleCloudBackup.clicked.connect(
            self.recording_controller.toggle_cloud_backup
        )

        # TERMINAL CONTROLLER
        self.ui.btn_clearTerminal.clicked.connect(self.terminal_controller.clear)

        # CONNECTION CONTROLLER
        self.ui.btn_toggleAutoReconnection.clicked.connect(
            self.connection_controller.toggle_auto_reconnect
        )
        self.ui.btn_connectBtn.clicked.connect(
            self.connection_controller.connect_disconnect_action
        )
        self.ui.terminal_input.returnPressed.connect(
            self.connection_controller.send_data_action
        )
        self.ui.btn_terminalSend.clicked.connect(
            self.connection_controller.send_data_action
        )

        #
        self.ui.btn_reloadWIndow.clicked.connect(self.reload_window)
        self.ui.cb_bauds.currentIndexChanged.connect(self.on_bauds_changed)
        self.ui.cb_ports.currentIndexChanged.connect(self.on_port_changed)

    def reload_window(self):
        """
        Reload the window and start it again
        """
        self.close()
        self.__init__()

    def on_bauds_changed(self):
        new_bauds = self.ui.cb_bauds.currentText()
        self.preferences.update("HIDDEN.last_bauds", new_bauds, 1)

    def on_port_changed(self):
        new_port = self.ui.cb_ports.currentText()
        self.preferences.update("HIDDEN.last_port", str(new_port), 1)
