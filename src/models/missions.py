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
import json
import typing

from PyQt5.QtCore import QObject, QThread

from src.ui import MissionForm


class MissionModel(QObject):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.ui = parent.ui
        self.preferences = parent.preferences

        self.all_missions = None

        self.setup_mission()

    def fetch_missions(self):
        self.all_missions = self.preferences.get("MISSIONS", 3)

    def setup_mission(self):
        self.fetch_missions()

        for mission, mission_data in self.all_missions.items():
            name = mission_data.get("name")
            description = mission_data.get("description")

            widget = MissionForm(self.parent, name, description)

            self.ui.layout_missionContainer.addWidget(widget)

    def create_new_mission(self):
        thread = self.CreateMissionThread(self)
        thread.start()

    def start_mission(self):
        print("Startin new Mission")

    class CreateMissionThread(QThread):
        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.preferences = parent.preferences

        def run(self):
            name = input("mission_name> ")
            desc = input("mission_description> ")
            formated_name = name.replace(" ", "_")

            with open("./src/config/missions/missions.json", "r") as file:
                data = json.load(file)

            # Add a new mission
            new_mission = {
                "NEW_MISSION": {
                    "name": name,
                    "description": desc,
                }
            }

            data["MISSIONS"].update(new_mission)

            # Write the updated data back to mission.json
            with open("mission.json", "w") as file:
                json.dump(data, file, indent=4)

            preferences = self.preferences.get("PREFERENCES", 1)
            new_preferences = {}

            for category, category_data in preferences.items():
                for preference_key, preference_value in category_data.items():
                    if preference_key == "link_google_account":
                        continue

                    preference_name = preference_key
                    preference_value = preference_value["value"]
                    new_preferences[preference_name] = preference_value

            with open(
                f"./src/config/missions/settings/{formated_name}.json", "w"
            ) as json_file:
                json.dump(new_preferences, json_file)
