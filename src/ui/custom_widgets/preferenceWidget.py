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
import os
import subprocess

from PyQt5.QtWidgets import QWidget

from ..generated_files.settings import Ui_SettingsForm


class PreferenceWidget(QWidget):
    def __init__(
        self,
        parent,
        name="default",
        description="default description",
        config_name=None,
        data_type=None,
        data=None,
    ) -> None:
        super(PreferenceWidget, self).__init__(parent)
        self.ui = Ui_SettingsForm()
        self.ui.setupUi(self)
        self.config_name = config_name
        self.parent = parent
        self.ui.label_config_name.setText(name)
        self.ui.description_label.setText(description)

        # Hide all widgets initially
        self.ui.integer.hide()
        self.ui.toggle.hide()
        self.ui.options.hide()
        self.ui.string.hide()
        self.ui.misc.hide()

        self.widget = None

        current_value = self.parent.preferences.get_preference(self.config_name)

        if data_type == "int":
            # Integer setting type
            self.ui.integer.show()
            self.ui.spinBox.setValue(current_value)
            self.ui.spinBox.valueChanged.connect(self.update_spinbox_config)

        elif data_type == "edit_string":
            # String setting type
            self.ui.string.show()
            self.ui.string.setText(current_value)
            self.ui.string.textEdited.connect(self.update_text_config)

        elif data_type == "toggle":
            # Toggle (boolean) setting type
            self.ui.toggle.show()
            if current_value:
                self.ui.btn_off.setChecked(False)
                self.ui.btn_on.setChecked(True)
            else:
                self.ui.btn_off.setChecked(True)
                self.ui.btn_on.setChecked(False)

            self.ui.btn_off.clicked.connect(self.update_toggle_button)
            self.ui.btn_on.clicked.connect(self.update_toggle_button)

        elif data_type == "open_folder":
            # File path setting type
            self.ui.misc.show()
            self.ui.misc.setText("Open Folder")
            self.ui.misc.clicked.connect(self.open_folder_action)

        elif data_type == "open_file":
            # File path setting type
            self.ui.misc.show()
            self.ui.misc.setText("Open File")
            self.ui.misc.clicked.connect(self.open_file_config)

        elif data_type == "connect_to_drive":
            # File path setting type
            self.ui.misc.show()
            self.ui.misc.setMinimumWidth(220)
            self.ui.misc.setMaximumWidth(220)
            self.ui.misc.setText("Link Google Account")
            self.ui.misc.clicked.connect(self.save_credentials)

        elif data_type == "toggle_widget":
            self.ui.toggle.show()
            widget_name = data.get("widget")
            self.widget = getattr(
                self.parent.ui, widget_name, None
            )  # Get the widget reference using getattr
            if current_value:
                self.ui.btn_off.setChecked(False)
                self.ui.btn_on.setChecked(True)
            else:
                self.ui.btn_off.setChecked(True)
                self.ui.btn_on.setChecked(False)

            self.ui.btn_off.clicked.connect(self.toggle_widget)
            self.ui.btn_on.clicked.connect(self.toggle_widget)

        elif data_type == "select_dashboard":
            # Dropdown (combobox) setting type for changing profiles
            self.ui.options.show()
            list_of_options = []

            data = self.parent.preferences.get("DASHBOARDS", 2)
            for option in data:
                list_of_options.append(option)

            self.ui.options.addItems(list_of_options)
            self.ui.options.setCurrentText(str(current_value))
            self.ui.options.currentIndexChanged.connect(self.update_profile_config)

    def open_file_config(self):
        # Get the file path from the configuration using self.config_name
        file_path = self.parent.preferences.get_preference(self.config_name)
        if file_path:
            # Open the file in the default text editor
            try:
                subprocess.run(["start", "", file_path], shell=True)
            except FileNotFoundError as e:
                raise Exception(f"Error: Default text editor not found: {e}")
            except Exception as e:
                raise Exception(f"Error: {e}")

            # Save the relative path to the function or configuration (adjust as per your requirement)
            relative_path = os.path.relpath(file_path)
            self.file_path = relative_path

    def open_folder_action(self):
        folder_path = self.parent.preferences.get_preference(self.config_name)
        if folder_path:
            # Open the folder in the default file explorer
            try:
                os.system(f'explorer "{folder_path}"')  # For Windows
                # For Linux, you can use: os.system(f'xdg-open "{folder_path}"')
            except Exception as e:
                raise Exception(f"Error: {e}")

            # Save the relative path to the function or configuration (adjust as per your requirement)
            relative_path = os.path.relpath(folder_path)
            self.folder_path = relative_path

    def update_spinbox_config(self):
        # Update the integer value in the configuration
        value = self.ui.spinBox.value()
        self.parent.preferences.update_preference(self.config_name, int(value))

    def update_text_config(self):
        # Update the string value in the configuration
        value = self.ui.string.text()
        self.parent.preferences.update_preference(self.config_name, str(value))

    def update_toggle_button(self):
        current_value = self.parent.preferences.get_preference(self.config_name)
        new_value = not current_value

        if new_value:
            self.ui.btn_on.setChecked(True)
            self.ui.btn_off.setChecked(False)

        else:
            self.ui.btn_on.setChecked(False)
            self.ui.btn_off.setChecked(True)

        self.parent.preferences.update_preference(self.config_name, new_value)

    def update_profile_config(self):
        # Update the selected profile in the configuration
        value = self.ui.options.currentText()
        self.parent.preferences.update_preference(self.config_name, str(value))
        self.parent.visualization_model.dashboards.switch_dashboard()

    def toggle_widget(self):
        current_value = self.parent.preferences.get_preference(self.config_name)
        new_value = not current_value

        if new_value:
            self.ui.btn_on.setChecked(True)
            self.ui.btn_off.setChecked(False)

        else:
            self.ui.btn_on.setChecked(False)
            self.ui.btn_off.setChecked(True)

        self.parent.preferences.update_preference(self.config_name, new_value)

        if self.widget is not None:
            if new_value:
                self.widget.show()
            else:
                self.widget.hide()

    def save_credentials(self):
        self.parent.cloud_manager.get_new_credentials()

    def test(self):
        self.parent.graph_manager.update_config_color()
