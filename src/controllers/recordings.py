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
from ..models.recordings import RecordingModel


class RecordingController:
    def __init__(self, parent):
        self.parent = parent
        self.preferences = parent.preferences

        # TEMPORAL (

        self.mission = "NO_MISSION"

        # )

        self.recordings_enabled = False
        self.recordings_model = RecordingModel(parent)
        self.cloud_backup_enabled = not self.preferences.get("HIDDEN.cloud_backup", 1)

        self.toggle_cloud_backup()

    def toggle_recordings(self):
        self.recordings_enabled = not self.recordings_enabled

        if self.recordings_enabled:
            self.recordings_model.reset_log_file(self.mission)

        else:
            if self.parent.cloud_model.logged_in:
                self.parent.cloud_model.upload_recording(
                    self.recordings_model.current_recording_file_path
                )

        if self.parent.cloud_model.logged_in:
            self.parent.ui.btn_toggleCloudBackup.setEnabled(self.recordings_enabled)

    def toggle_cloud_backup(self):
        self.cloud_backup_enabled = not self.cloud_backup_enabled
        self.parent.ui.btn_toggleCloudBackup.setChecked(self.cloud_backup_enabled)
        self.preferences.update("HIDDEN.cloud_backup", self.cloud_backup_enabled, 1)
