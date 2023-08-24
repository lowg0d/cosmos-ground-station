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

"""
This module provides a QObejct class, SerialModel, for managing
serial communication with connected devices. It also includes a thread,
SerialReadThread, for reading data from the serial port concurrently, that also emits
the data to the update_value_chain, adn write_to_terminal signals.
"""

import serial
import serial.tools.list_ports as list_port_tool

from PyQt5.QtCore import QObject, pyqtSignal, QThread

from src.controllers.recordings import RecordingController

class SerialModel(QObject):
    """
    This class manages serial communication with connected devices
    and includes a thread for concurrent data reading.
    """

    write_to_terminal = pyqtSignal(str)
    update_value_chain = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.recording_model = None

        self.worker = None
        self.ser = serial.Serial(timeout=1)

        self.packet_header = str(
            self.parent.parent.preferences.get_preference("packet.signature_header")
        )
        self.packet_split_char = str(
            self.parent.parent.preferences.get_preference("packet.split_char")
        )

        self.is_connected = False
        self.port_list = []

    def update_ports(self):
        """
        Retrieves a list of available serial ports and stores them in the 'port_list' attribute.
        """
        self.port_list = [port.device for port in list_port_tool.comports()]

    def open_serial(self):
        """
        Attempt to open the serial port.
        """
        try:
            self.ser.open()
            self.is_connected = True

            self.start_read_thread()
            return True, ""

        except serial.SerialException:
            return False, "Device Disconnected Or Already Connected"

    def close_serial(self):
        """
        Attempt to close the serial port.
        """
        self.stop_read_thread()
        self.ser.close()

        self.is_connected = False

    def send_data(self, data):
        """
        Sends data over the serial port.
        """
        try:
            b_data = data.encode("utf-8")  # Convert data to bytes
            self.ser.write(b_data)

        except serial.SerialException as exc:
            self.parent.window_controller.show_error_dialog(
                "Error Sending Data To The Serial Port", str(e)
            )

    def read_data(self):
        """
        Reads and processes data from the serial port.
        """
        try:
            rcv_data = str(self.ser.readline().decode("utf-8"))

        except UnicodeDecodeError as exc:
            raise UnicodeError from exc

        if len(rcv_data) > 2:
            if rcv_data.startswith(self.packet_header):
                data_formated = rcv_data.replace(f"{self.packet_header}", "")
                self.write_to_terminal.emit(data_formated)

    # THREAD

    def handle_thread_stop(self):
        if self.is_connected:
            self.parent.connect_disconnect_action()

    def start_read_thread(self):
        self.worker = self.SerialReadThread(self)
        self.worker.start()

    def stop_read_thread(self):
        self.worker.terminate()

    class SerialReadThread(QThread):
        """
        This class represents a thread for reading serial data from a connected device.
        """

        finished = pyqtSignal()

        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.finished.connect(self.parent.handle_thread_stop)

        def run(self):
            """
            The main execution logic of the thread.
            Reads data from the serial port as long as the parent's 'is_connected' flag is True,
            when not it emits the finished signal, that will call the disconnect function.
            """
            while self.parent.is_connected:
                if self.parent.ser.isOpen():
                    try:
                        self.parent.read_data()

                    except serial.serialutil.SerialException as exc:
                        if "Access is denied" in str(exc):
                            self.parent.ser.close()

                        else:
                            print(f"Error in Reading Thread: {exc}")

                else:
                    break

            self.finished.emit()
