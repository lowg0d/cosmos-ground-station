#############################################################
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
"""
This module defines the `MainWindow` class, which serves as the central component of the Cosmos.
Encapsulates various UI components and controllers for the gui.
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QLabel, QShortcut
from qframelesswindow import FramelessMainWindow

from src.controllers import (
    ConnectionController,
    RecordingController,
    TerminalController,
    WindowController,
)
from src.models import (
    CloudModel,
    DataHandlerModel,
    MissionModel,
    PreferenceModel,
    SerialModel,
    VisualizationModel,
)
from src.ui import CustomTitleBar, PreferenceWidget, Ui_MainWindow


class MainWindow(FramelessMainWindow):
    """
    Core class managing UI elements, preferences, and controllers.
    Handles user interactions for connections, terminals, and window behavior.
    """

    def __init__(self) -> None:
        super().__init__()
        # Set a custom title bar for the window
        self.setTitleBar(CustomTitleBar(self))

        # Setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize models
        self.preferences = PreferenceModel()
        self.serial_model = SerialModel(self)
        self.missions_model = MissionModel(self)
        self.cloud_model = CloudModel(self)
        self.recording_controller = RecordingController(self)
        self.data_handler_model = DataHandlerModel(self)

        # Initialize Controllers
        self.window_controller = WindowController(self)
        self.terminal_controller = TerminalController(self)

        self.visualization_model = VisualizationModel(self)
        self.connection_controller = ConnectionController(self)

        if not self.window_controller.small_mode_toggled:
            self.showMaximized()

        # Get the application information from preferences
        self.name = self.preferences.get("name")
        self.version = self.preferences.get("version")
        self.dev_phase = self.preferences.get("dev_phase")
        self.author = self.preferences.get("author")

        # Set up window properties
        self.setWindowIcon(QIcon(self.preferences.get("icon")))
        self.setWindowTitle(self.name.upper())

        # Update the labels that display the info of the application
        self.ui.label_statusBar.setText(f"v{self.version}-{self.dev_phase}")

        self.ui.label_longVersion.setText(
            f'Version: {self.version}-{self.dev_phase} - Author: {self.author} - Help: <a href="https://github.com/lowg0d/cosmos-ground-station">Find Help or report a Bug</a>'
        )
        self.ui.label_longVersion.setOpenExternalLinks(True)

        # Connect the signals of the buttons with controllers functions
        self.setup_signals()

        # Convert the preference file into interactive widgets for easy configuration modification.
        self.generate_ui_preferences_widgets()

        # change the page to the dashboard
        self.ui.stackedWidget_central.setCurrentWidget(self.ui.page_centralDashboard)

        # Adjust splitter sizes
        self.ui.splitter.setSizes([6000, 100])

        self.ui.progress_bar_statusBar.hide()

        # raise titlebar, show the window and maximize it.
        self.titleBar.raise_()
        self.show()

    def generate_ui_preferences_widgets(self):
        preferences_data = self.preferences.get("PREFERENCES", 1)

        for category, items in preferences_data.items():
            # Create a label for the category
            category_label = QLabel(f"# {category.upper()}")
            self.ui.layout_preferences.addWidget(category_label)

            for name, setting_data in items.items():
                full_setting_name = f"{category}.{name}"

                # Create a widget for the setting
                setting_widget = PreferenceWidget(
                    self,
                    name=setting_data.get("name"),
                    description=setting_data.get("description"),
                    config_name=full_setting_name,
                    data_type=setting_data.get("preference_type"),
                    data=setting_data,
                )
                self.ui.layout_preferences.addWidget(setting_widget)

    def setup_signals(self):
        # signal from data handler to the terminal
        self.data_handler_model.write_to_terminal.connect(
            self.terminal_controller.write
        )

        self.data_handler_model.update_value_chain.connect(
            self.visualization_model.updates.update_value_chain
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

        self.ui.btn_missionDisplay.clicked.connect(
            self.window_controller.toggle_mission_page
        )

        self.ui.btn_GoBack2.clicked.connect(self.window_controller.toggle_mission_page)

        #
        self.ui.btn_reloadWIndow.clicked.connect(self.restart)
        self.ui.cb_bauds.currentIndexChanged.connect(self.on_bauds_changed)
        self.ui.cb_ports.currentIndexChanged.connect(self.on_port_changed)

    @staticmethod
    def restart():
        MainWindow.singleton = MainWindow()

    def on_bauds_changed(self):
        new_bauds = self.ui.cb_bauds.currentText()
        self.preferences.update("HIDDEN.last_bauds", new_bauds, 1)

    def on_port_changed(self):
        new_port = self.ui.cb_ports.currentText()
        self.preferences.update("HIDDEN.last_port", str(new_port), 1)
