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
from src.ui import MissionForm


class MissionModel:
    def __init__(self, parent):
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
        print("Startin new Mission")

    def start_mission(self):
        print("Startin new Mission")
