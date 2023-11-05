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
from datetime import datetime

import serial
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class DataHandlerModel(QObject):
    write_to_terminal = pyqtSignal(str)
    update_value_chain = pyqtSignal(list)

    send_notification = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.unknown_header_first_time = False
        self.serial_model = parent.serial_model
        self.recording_model = parent.recording_controller.recordings_model

        self.packet_header = str(
            self.parent.preferences.get_preference("packet.signature_header")
        )
        self.message_header = str(
            self.parent.preferences.get_preference("packet.msg_signature_header")
        )
        self.packet_split_char = str(
            self.parent.preferences.get_preference("packet.split_char")
        )

        self.value_chain = []

    def handle_thread_stop(self):
        if self.serial_model.is_connected:
            self.parent.connection_controller.connect_disconnect_action()

    def start_thread(self):
        self.worker = self.SerialReadThread(self)
        self.worker.error.connect(self.error_notification)
        self.worker.start()

    def error_notification(self, msg):
        self.parent.notifications.new(
            msg=msg,
            level="error",
            duration="permanent",
        )

    def stop_thread(self):
        self.worker.terminate()

    class SerialReadThread(QThread):
        """
        This class represents a thread for reading serial data from a connected device.
        """

        finished = pyqtSignal()
        error = pyqtSignal(str)

        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.header_error = False
            self.finished.connect(self.parent.handle_thread_stop)

        def run(self):
            """
            Reads data from the serial port as long as the parent's 'is_connected' flag is True,
            when not it emits the finished signal, that will call the disconnect function.

            This is thought so i can change where the data is comming from, so i can add a simulation mode
            and get data from another cosmos, using sockets or something similar.
            """

            while self.parent.serial_model.is_connected:
                if self.parent.serial_model.ser.isOpen():
                    try:
                        data = str(self.get_serial_data())

                    except serial.serialutil.SerialException:
                        self.parent.serial_model.ser.close()

                    if data != UnicodeDecodeError:
                        self.process_data(data)

                    else:
                        self.error.emit("Skipping Corrupt Packet, Unable To Decode.")

                else:
                    break

            self.finished.emit()

        def get_serial_data(self):
            data = self.parent.serial_model.read_data()
            return data

        def process_data(self, rcv_data):
            now = datetime.now().strftime("%d.%m.%Y;%H.%M.%S.%f")

            if len(rcv_data) > 2:
                if rcv_data.startswith(self.parent.packet_header):
                    if self.header_error:
                        self.header_error = False

                    formated = rcv_data.replace(self.parent.packet_header, "")
                    value_chain = (
                        str(formated).strip().split(f"{self.parent.packet_split_char}")
                    )

                    # emit signals
                    self.parent.update_value_chain.emit(value_chain)
                    self.parent.write_to_terminal.emit(str(value_chain))

                    if self.parent.parent.recording_controller.recordings_enabled:
                        self.parent.recording_model.write_to_log_file(now, value_chain)

                elif rcv_data.startswith(self.parent.message_header):
                    self.parent.send_notification.emit(
                        rcv_data.replace(self.parent.message_header, "")
                    )

                else:
                    if rcv_data != UnicodeDecodeError:
                        if not self.header_error:
                            self.header_error = True
                            self.error.emit(
                                f"Packet With Unknown Signature Header, Change In Settings"
                            )

                    else:
                        self.error.emit("Skipping Corrupt Packet, Unable To Decode.")

            # write everything to backup file
            self.parent.recording_model.write_to_blackbox(now, rcv_data)
