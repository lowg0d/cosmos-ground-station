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
import time


class RecordingController:

    def __init__(self, parent):
        self.parent = parent

        self.recordings_enabled = False
        self.cloud_backup_enabled = False

        self.current_file = None

        self.recordings_path = self.parent.preferences.get_preference("recordings.path")
        self.current_file_path = f"{self.recordings_path}/default.csv"
        self.blackbox_path = f"{self.recordings_path}/blackbox"

        self.check_paths()

    def check_paths(self):
        """
        Ensure that the folder exists
        """
        os.makedirs(self.recordings_path, exist_ok=True)
        os.makedirs(self.blackbox_path, exist_ok=True)

    def toggle_recordings(self):
        """
        Toggle if save the information or not
        """
        if self.recordings_enabled:
            if self.cloud_backup_enabled:
                self.upload_cloud_backup()

        else:
            self.parent.ui.btn_toggleRecordings.setChecked(True)
            self.start_recording_file()

        self.recordings_enabled = not self.recordings_enabled
        self.parent.ui.btn_toggleRecordings.setChecked(self.recordings_enabled)

    def start_recording_file(self):
        """
        Start a new recording file
        """

        recording_date = time.strftime("%d.%m.%y")
        recording_id_number = 0
        recording_id = f"{recording_date}-{recording_id_number}"
        current_path = f"{self.recordings_path}/rec-{recording_id}.csv"

        while os.path.exists(current_path):
            recording_id_number += 1
            recording_id = f"{recording_date}-{recording_id_number}"
            current_path = f"{self.recordings_path}/rec-{recording_id}.csv"

        self.current_file_path = current_path
        self.current_file = open(self.current_file_path, "w", encoding="utf-8")

    def reset_blackbox_file(self):
        pass

    def toggle_cloud_backup(self):
        """
        toggle the cloud backup, when the log is disabled it will upload it automatically
        """
        self.cloud_backup_enabled = not self.cloud_backup_enabled
        self.parent.ui.btn_toggleCloudBackup.setChecked(self.cloud_backup_enabled)
        self.parent.ui.btn_toggleCloudBackup.setEnabled(self.cloud_backup_enabled)

    def write_to_recording_file(self, now, value_list):
        """
        write a new entry to the current recording file
        """
        current_time = now.strftime("%H:%M:%S:%f")
        value_list.append(current_time)

        try:
            with open(
                self.recordings_path, "a", newline="", encoding="utf"
            ) as recording_file:
                writer = csv.writer(recording_file, delimiter=",", encoding="utf-8")
                writer.writerow(value_list)

        except Exception as exc:
            print(f"Error writing to recording file: {exc}")

    def write_to_blackbox(self, now, value_list):
        """
        write a new entry to the current recording file
        """
        current_time = now.strftime("%H:%M:%S:%f")
        value_list.append(current_time)

        try:
            with open(
                self.blackbox_path, "a", newline="", encoding="utf"
            ) as recording_file:
                writer = csv.writer(recording_file, delimiter=",", encoding="utf-8")
                writer.writerow(value_list)

        except Exception as exc:
            print(f"Error writing to recording file: {exc}")

    def upload_cloud_backup(self):
        print("uploading cloud backup...")
