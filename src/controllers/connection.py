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

"""
This module defines the ConnectionController class responsible for managing the
connection and communication with a serial port.
It handles port detection, connection establishment, data sending, and error handling.
"""

from PyQt5.QtCore import QObject, QTimer
from src.models.serial import SerialModel


class ConnectionController(QObject):
    """
    This class manages the connection and communication with a serial port.
    It provides methods to handle port detection, connection establishment, data sending,
    and error handling.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.serial_model = self.parent.serial_model
        self.data_handler_model = self.parent.data_handler_model

        self.last_port_list = []
        self.current_selected_port = None
        self.reconnection_port = None
        self.reconnection_enabled = self.parent.preferences.get(
            "HIDDEN.auto_reConnect", 1
        )

        if self.reconnection_enabled:
            self.parent.ui.btn_toggleAutoReconnection.setChecked(True)

        bauds_options = {
            "1200": 1200,
            "2400": 2400,
            "4800": 4800,
            "9600": 9600,
            "19200": 19200,
            "38400": 38400,
            "57600": 57600,
            "115200": 115200,
        }

        self.parent.ui.cb_bauds.addItems(bauds_options.keys())
        self.parent.ui.cb_bauds.setCurrentText(
            self.parent.preferences.get("HIDDEN.last_bauds", 1)
        )

        self.new_port_detect_timer = QTimer()
        self.new_port_detect_timer.timeout.connect(self.new_port_detector)
        self.new_port_detect_timer.start(200)

        self.update_ports_action()

    def new_port_detector(self):
        """
        Connected to a timer to automatically update ports. If a new port is detected,
        updates the ComboBox that shows it. If reconnection is enabled and the
        last selected port is available, automatically connects to it, if theare are no
        ports available it disables the connect button.
        """
        if len(self.serial_model.port_list) == 0:
            if self.parent.ui.btn_connectBtn.isEnabled:
                self.parent.ui.btn_connectBtn.setEnabled(False)

        else:
            if not self.parent.ui.btn_connectBtn.isEnabled():
                self.parent.ui.btn_connectBtn.setEnabled(True)

        if self.serial_model.port_list != self.last_port_list:
            self.last_port_list = self.serial_model.port_list
            self.update_ports_action()

            if (
                self.reconnection_enabled
                and self.reconnection_port in self.serial_model.port_list
            ):
                index = self.serial_model.port_list.index(self.reconnection_port)
                self.parent.ui.cb_ports.setCurrentIndex(index)
                self.connect_disconnect_action()

        else:
            self.serial_model.update_ports()

    def update_ports_action(self):
        """
        Updates the list of ports available on the computer in the combo box.
        If ports are available, sets the default port index based on the last selected port,
        saved in preferences.
        """
        self.serial_model.update_ports()  # Update the list of ports
        self.parent.ui.cb_ports.clear()  # Clear the combo box

        if self.serial_model.port_list:
            self.parent.ui.cb_ports.addItems(
                self.serial_model.port_list
            )  # Add available ports

            # Set default port index in the combo box
            last_port = self.parent.preferences.get("HIDDEN.last_port", 1)

            if last_port in self.serial_model.port_list:
                index = self.serial_model.port_list.index(last_port)
                self.parent.ui.cb_ports.setCurrentIndex(
                    index
                )  # Set index to the last used port
            else:
                self.parent.ui.cb_ports.setCurrentIndex(
                    0
                )  # Set index to the first port if last used port not found

    def connect_disconnect_action(self):
        """
        Handles connecting and disconnecting actions based on the current state.
        If connected, disconnects, resets UI, and stops data handling timers.
        If disconnected, opens the serial port, starts data handling timers, and updates UI.
        """
        self.current_selected_port = self.parent.ui.cb_ports.currentText()

        # Disconnect
        if self.serial_model.is_connected:
            self.parent.visualization_model.change_to_disconnected()
            self.data_handler_model.stop_thread()

            self.serial_model.close_serial()
            

            self.parent.window_controller.set_default_look()  # Reset UI
            self.parent.terminal_controller.write(
                "<b style='color:#a8002a;'>[ DISCONNECTED ]</b>"
            )

        # Connect
        else:
            # Set serial port settings
            self.serial_model.ser.port = self.current_selected_port
            self.serial_model.ser.baudrate = int(self.parent.ui.cb_bauds.currentText())

            (
                succes,
                message,
            ) = self.serial_model.open_serial()  # Connect to the serial port
            if succes:
                # Update UI and terminal
                self.parent.window_controller.set_connected_look(
                    self.current_selected_port
                )
                self.parent.terminal_controller.write(
                    "<b style='color:#8cb854;'>[ CONNECTED ]</b>"
                )

                if self.reconnection_enabled:
                    self.reconnection_port = self.current_selected_port

                self.data_handler_model.start_thread()
                self.parent.visualization_model.change_to_connected()

            else:
                self.handle_connection_error(message)
            

    def handle_connection_error(self, message=None):
        """
        Handles errors that occur during connection attempts.
        Displays the error message in the terminal.
        """
        self.update_ports_action()  # Update ports list in UI
        self.parent.window_controller.set_default_look()

        if message:
            self.parent.terminal_controller.write(
                "<b style='color:#a8002a;'>[ ERROR CONNECTING ]</b>"
                + f" - <b style='color:#a8002a;'>{message}</b>"
            )
        else:
            self.parent.terminal_controller.write(
                "<b style='color:#a8002a;'>[ ERROR CONNECTING ]</b>"
            )

    def send_data_action(self, custom_data=None):
        """
        Sends data to the connected serial port. If custom_data is provided,
        sends that data. Otherwise, sends the data from the UI's input field.
        """
        if custom_data is not None:
            data = str(custom_data)
        else:
            data = self.parent.ui.terminal_input.text()
            self.parent.ui.terminal_input.setText("")  # Clear the input field
        
        if self.serial_model.is_connected:
            if len(data) > 0:
                self.serial_model.send_data(data)  # Send data through the serial port
                self.parent.terminal_controller.write(
                    f"<ins style='color:#8cb854';>[ Sended -> ]:</ins> '{data}'"
                )
            else:
                self.parent.terminal_controller.write(
                    "<b style='color:#a8002a';>[ Nothing To Send ]</b>"
                )
        else:
            self.parent.terminal_controller.write(
                "<b style='color:#a8002a';>[ Not Connected ] </b>"
            )

    def toggle_auto_reconnect(self):
        """
        This function toggles the auto-reconnect feature based on the current state.
        """
        if self.reconnection_enabled:
            self.parent.ui.btn_toggleAutoReconnection.setChecked(False)
            self.parent.preferences.update("HIDDEN.auto_reConnect", False, 1)
            self.reconnection_port = None
            self.reconnection_enabled = False
        else:
            self.parent.ui.btn_toggleAutoReconnection.setChecked(True)
            self.parent.preferences.update("HIDDEN.auto_reConnect", True, 1)
            self.reconnection_port = self.parent.ui.cb_ports.currentText()
            self.reconnection_enabled = True
