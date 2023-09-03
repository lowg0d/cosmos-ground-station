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

import os
import csv


class RecordingModel:
    """
    This Mmodule managers recordings
    """

    def __init__(self, parent):
        self.parent = parent

        self.recording_save_path = self.parent.preferences.get_preference(
            "recordings.path"
        )
        self.blackbox_file_path = (
            f"{self.recording_save_path}/last_conn/last_connection.txt"
        )
        self.current_recording_file_path = f"{self.recording_save_path}/default.csv"

        self.reset_blackbox()

        self.check_paths_existance()

    def check_paths_existance(self):
        os.makedirs(self.recording_save_path, exist_ok=True)

    def reset_blackbox(self):
        with open(self.blackbox_file_path, "w", encoding="utf-8") as f:
            f.close()

    def write_to_blackbox(self, packet_time, data):
        """
        This functions gets called whenever a packet is received from the serial,
        it writes all the data, and the time it occured in a backup file that is created
        every time a connection is established.
        """
        try:
            with open(self.blackbox_file_path, "a", encoding="utf-8") as blackbox_file:
                blackbox_file.write(f"{data}, {packet_time}")

        except Exception as exc:
            self.parent.window_controller.show_error_dialog(
                "Exception Writing Backup File", exc
            )
