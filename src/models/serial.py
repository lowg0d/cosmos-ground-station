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


class SerialModel:
    """
    This class manages serial communication with connected devices
    and includes a thread for concurrent data reading.
    """

    def __init__(self, parent):
        self.parent = parent
        self.ser = serial.Serial(timeout=1)

        self.is_connected = False
        self.port_list = []

    def update_ports(self):
        """
        Retrieves a list of available serial ports and stores them in the 'port_list' attribute.
        """
        self.port_list = [port.device for port in list_port_tool.comports()]

    def open_serial(self):
        try:
            self.ser.open()
            self.is_connected = True
            return True, ""

        except serial.SerialException:
            return False, "Device Disconnected Or Already Connected"

    def close_serial(self):
        self.ser.close()
        self.is_connected = False

    def send_data(self, data):
        try:
            b_data = data.encode("utf-8")  # Convert data to bytes
            self.ser.write(b_data)

        except serial.SerialException as exc:
            self.parent.window_controller.show_error_dialog(
                "Error Sending Data To The Serial Port", str(exc)
            )

    def read_data(self) -> None:
        try:
            rcv_data = str(self.ser.readline().decode("utf-8"))
            return rcv_data

        except UnicodeDecodeError:
            print(f"[-] Packet Corrupted, can't parse data.")
