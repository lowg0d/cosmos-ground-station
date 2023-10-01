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
import datetime
import csv


class RecordingModel:
    def __init__(self, parent):
        self.parent = parent
        self.recording_save_path = self.parent.preferences.get_preference(
            "data.recordings_path"
        )
        self.blackbox_file_path = os.path.join(
            self.recording_save_path, "last_connection.txt"
        )
        self.current_recording_file_path = os.path.join(
            self.recording_save_path, "default.csv"
        )
        self.reset_blackbox()
        self.check_paths_existence()

    def check_paths_existence(self):
        os.makedirs(self.recording_save_path, exist_ok=True)

    def reset_blackbox(self):
        open(self.blackbox_file_path, "w", encoding="utf-8").close()

    def write_to_blackbox(self, packet_time, data):
        save_string = f"{packet_time}/{data}"
        try:
            with open(self.blackbox_file_path, "a", encoding="utf-8") as blackbox_file:
                blackbox_file.write(save_string)
        except Exception as exc:
            raise Exception("Exception Writing Backup File", exc)

    def reset_log_file(self, current_mission):
        date = datetime.datetime.now().strftime("%d.%m.%Y")
        id_ = 0
        file_id = f"{date}-{id_}"
        path = os.path.join(self.recording_save_path, current_mission, f"{file_id}.csv")

        os.makedirs(
            os.path.join(self.recording_save_path, current_mission), exist_ok=True
        )

        while os.path.exists(path):
            id_ += 1
            file_id = f"{date}-{id_}"
            path = os.path.join(
                self.recording_save_path, current_mission, f"{file_id}.csv"
            )

        self.current_recording_file_path = path

    def write_to_log_file(self, now, data):
        data.append(now)
        try:
            with open(
                self.current_recording_file_path, "a", newline="", encoding="utf-8"
            ) as recording_file:
                writer = csv.writer(recording_file, delimiter=",")
                writer.writerow(data)
        except Exception as e:
            raise Exception(f"Error writing to recording file: {e}")
