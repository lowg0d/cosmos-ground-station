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
"""
This modules is used to get and edit data from the confuration file.
Also it provides functions to access the preferences inside the custom preferences.json file.
"""

import json
import os
import tempfile


class PreferenceModel:
    def __init__(self):
        self.paths = [
            "./src/config/app.json",
            "./src/config/preferences/preferences.json",
            "./src/config/visualization/dashboards.json",
            "./src/config/missions/missions.json",
            "./src/config/themes.json",
        ]
        self.preference_path = 1

    def load_file(self, path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def get(self, data_key, path_index=0, not_exit=False):
        # check if the path index exits
        if path_index >= len(self.paths):
            exit(f"[{path_index}] is not a valid path index")

        # load the path
        path = self.paths[path_index]
        path_data = self.load_file(path)

        # get the value from nested files
        keys = data_key.split(".")
        for key in keys:
            # if key does not exist
            if key not in path_data:
                if not not_exit:
                    exit(f"[{data_key} ({key})] is not valid key")

                return "NotFound"

            path_data = path_data[key]

        return path_data

    def update(self, data_key, new_value, path_index):
        # check if the path index exits
        if path_index >= len(self.paths):
            exit(f"[{path_index}] is not a valid path index")

        # load the path
        path = self.paths[path_index]
        path_data = self.load_file(path)
        current = path_data
        keys = data_key.split(".")
        for key in keys[:-1]:
            # if key does not exist
            if key not in current:
                exit(f"[{data_key} ({key})] is not valid key")

            current = current[key]

        current[keys[-1]] = new_value
        with open(path, "w", encoding="utf-8") as file:
            json.dump(path_data, file, indent=2)

    def get_preference(self, data_key):
        path = self.paths[self.preference_path]
        path_data = self.load_file(path)
        keys = ("PREFERENCES." + data_key + ".value").split(".")

        for key in keys:
            if key not in path_data:
                exit(f"[{data_key} ({key})] is not a valid key")

            path_data = path_data[key]

        return path_data

    def update_preference(self, data_key, new_value):
        path = self.paths[self.preference_path]
        path_data = self.load_file(path)
        current = path_data
        keys = ("PREFERENCES." + data_key + ".value").split(".")

        for key in keys[:-1]:
            if key not in current:
                exit(f"[{data_key} ({key})] is not a valid key")

            current = current[key]

        current[keys[-1]] = new_value
        with open(path, "w", encoding="utf-8") as file:
            json.dump(path_data, file, indent=2)

    def get_json_from_file(self, data_key):
        path = self.paths[self.preference_path]
        path_data = self.load_file(path)
        keys = ("PREFERENCES." + data_key + ".value").split(".")

        for key in keys:
            if key not in path_data:
                exit(f"[{data_key} ({key})] is not a valid key")

            path_data = path_data[key]

        try:
            with open(path_data, "r") as f:
                txt = f.read()
                json_txt = json.loads(txt)
                return json_txt

        except FileNotFoundError:
            exit(f"[{path_data})] file does not exits")

        except json.JSONDecodeError:
            exit(f"[{path_data})] is not a valid file for json conversion")

        except Exception as e:
            exit(f"[Unknown Error] {e}")

    def save_preferences_to_temp(self):
        preferences = self.get("PREFERENCES", 1)
        new_preferences = {}

        for c, category_data in preferences.items():
            for preference_key, preference_value in category_data.items():
                if preference_key == "link_google_account":
                    continue

                preference_name = preference_key
                preference_value = preference_value["value"]
                new_preferences[preference_name] = preference_value

        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, "preferences_upload.json")

        with open(temp_file_path, "w") as json_file:
            json.dump(new_preferences, json_file)

        return temp_file_path
