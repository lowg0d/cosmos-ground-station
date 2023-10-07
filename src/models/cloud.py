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
import logging
import os

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from PyQt5.QtCore import QObject, QThread, pyqtSignal

SCOPES = ["https://www.googleapis.com/auth/drive"]
CLOUD_FILE_NAME = "COSMOS BACKUPS"


class CloudModel(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        logging.getLogger("googleapiclient").setLevel(logging.WARNING)
        logging.getLogger("google").setLevel(logging.WARNING)

        self.creds = None
        self.service = None
        self.folder_id = None
        self.main_folder_id = None
        self.logged_in = False

        self.user_mail = None
        self.binded_widget = None

    def bind_preference(self, widget):
        self.binded_widget = widget
        self.check_account()

    # LOGIN / LOGOUT

    def login(self):
        thread = self.GetCredentialsThread(self)
        thread.finished.connect(self.check_account)
        thread.start()

    def logout(self):
        if os.path.exists("./src/config/cloud/token.json"):
            os.remove("./src/config/cloud/token.json")

        self.check_account()

    class GetCredentialsThread(QThread):
        finished = pyqtSignal()  # Signal to indicate thread has finished

        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent

        def run(self):
            flow = InstalledAppFlow.from_client_secrets_file(
                "./src/config/cloud/private/credentials.json", SCOPES
            )
            self.parent.creds = flow.run_local_server(
                port=0,
            )

            with open("./src/config/cloud/token.json", "w") as token:
                token.write(self.parent.creds.to_json())

            self.finished.emit()  # Emit the finished signal

    # CHECK ACCOUNT
    class CheckAccountThread(QThread):
        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent

        def run(self):
            if os.path.exists("./src/config/cloud/token.json"):
                self.parent.creds = Credentials.from_authorized_user_file(
                    "./src/config/cloud/token.json", SCOPES
                )
                if not self.parent.creds.valid:
                    if (
                        self.parent.creds
                        and self.parent.creds.expired
                        and self.parent.creds._refresh_token
                    ):
                        self.parent.creds.refresh(Request())

                        with open("./src/config/cloud/token.json", "w") as token:
                            token.write(self.parent.creds.to_json())

                self.parent.logged_in = True

                self.parent.service = build(
                    "drive", "v3", credentials=self.parent.creds
                )

                self.parent.user_mail = self.parent.update_gmail()
                self.parent.update_pic()

                self.parent.main_folder_id = self.parent.get_folder(
                    "COSMOS", main_folder=True
                )
                self.parent.binded_widget.update_gmail(self.parent.user_mail)

            else:
                self.parent.logged_in = False

            self.parent.binded_widget.set_to_logged_in(self.parent.logged_in)

    def check_account(self):
        thread = self.CheckAccountThread(self)
        thread.start()

    def update_gmail(self):
        try:
            self.service = build("drive", "v3", credentials=self.creds)
            about = self.service.about().get(fields="user(emailAddress)").execute()
            gmail_address = about["user"]["emailAddress"]
            return gmail_address

        except HttpError as e:
            print(f"Error [{e}]")

    def update_pic(self):
        try:
            self.service = build("drive", "v3", credentials=self.creds)
            about = self.service.about().get(fields="user(photoLink)").execute()
            photo_link = about["user"]["photoLink"]

            # download photo to profile.jpg
            response = requests.get(photo_link)
            if response.status_code == 200:
                with open("./src/config/cloud/profile.jpg", "wb") as file:
                    file.write(response.content)
            else:
                print(
                    f"Error downloading profile picture. Status code: {response.status_code}"
                )

        except HttpError as e:
            print(f"Error [{e}]")

    # CHECK FOLDER
    # Create folder
    def get_folder(self, folder_name: str, main_folder=False):
        try:
            response = (
                self.service.files()
                .list(
                    q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                    spaces="drive",
                )
                .execute()
            )

            if not response["files"]:
                if main_folder:
                    file_metadata = {
                        "name": f"{folder_name}",
                        "mimeType": "application/vnd.google-apps.folder",
                    }

                else:
                    self.main_folder_id = self.get_folder("COSMOS", main_folder=True)
                    file_metadata = {
                        "name": f"{folder_name}",
                        "mimeType": "application/vnd.google-apps.folder",
                        "parents": [f"{self.main_folder_id}"],
                    }

                file_ = (
                    self.service.files()
                    .create(body=file_metadata, fields="id")
                    .execute()
                )

                folder_id = file_.get("id")

            else:
                folder_id = response["files"][0]["id"]

        except HttpError as e:
            print(f"Error [{e}]")

        return folder_id

    # UPLOAD
    class UploadFileThread(QThread):
        finished = pyqtSignal()  # Signal to indicate thread has finished

        def __init__(self, parent, path, mission):
            super().__init__(parent)
            self.parent = parent
            self.mission = mission
            self.path = path

        def run(self):
            if os.path.exists(self.path):
                upload_folder_id = self.parent.get_folder(f"{self.mission}-BACKUP")

                name = os.path.basename(self.path)
                file_metadata = {"name": name, "parents": [upload_folder_id]}
                media = MediaFileUpload(f"{self.path}")
                upload_file = (
                    self.parent.service.files()
                    .create(body=file_metadata, media_body=media, fields="id")
                    .execute()
                )

                print(f"[+] File Uploaded: {name}")

                self.finished.emit()  # Emit the finished signal

    def upload_recording(self, path, mission="NO_MISSION"):
        thread = self.UploadFileThread(self, path, mission)
        thread.start()
