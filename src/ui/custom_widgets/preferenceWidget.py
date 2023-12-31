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

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QWidget

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
        restart=False,
    ) -> None:
        super(PreferenceWidget, self).__init__(parent)
        self.ui = Ui_SettingsForm()
        self.ui.setupUi(self)
        self.config_name = config_name
        self.parent = parent
        self.restart = restart
        self.ui.label_config_name.setText(name)
        self.ui.description_label.setText(description)

        self.name = name
        self.description = description

        self.last_value = None

        # Hide all widgets initially
        self.ui.integer.hide()
        self.ui.toggle.hide()
        self.ui.options.hide()
        self.ui.string.hide()
        self.ui.misc.hide()
        self.ui.profile.hide()
        self.ui.folder.hide()
        self.ui.restart.hide()

        self.widget = None
        self.default_style = self.ui.misc.styleSheet()

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

        elif data_type == "folder":
            # File path setting type
            self.ui.misc.show()
            self.ui.folder.show()

            self.ui.misc.setText("Open")
            simplified_path = "/".join(
                current_value.split("/")[-2:]
            )  # Get the last two folders

            if len(simplified_path) > 20:
                simplified_path = simplified_path[:18] + "..."

            self.ui.folder.setText(simplified_path)

            self.ui.misc.clicked.connect(self.open_folder_action)
            self.ui.folder.clicked.connect(self.change_folder_action)

        elif data_type == "open_file":
            # File path setting type
            self.ui.misc.show()
            self.ui.misc.setText("Open File")
            self.ui.misc.clicked.connect(self.open_file_config)

        elif data_type == "google_login":
            # File path setting type
            self.parent.cloud_model.bind_preference(self)
            self.ui.misc.show()
            self.ui.misc.setEnabled(False)

            self.ui.description_label.setText(f"Loading Google Account Data...")
            self.ui.label_config_name.setText(f"Loading Google Account...")
            self.ui.misc.setText("Loading...")

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

                self.widget.hide()

            self.ui.btn_off.clicked.connect(self.toggle_widget)
            self.ui.btn_on.clicked.connect(self.toggle_widget)

        elif data_type == "select_dashboard":
            # Dropdown (combobox) setting type for changing profiles
            self.ui.options.show()
            self.ui.misc.show()

            self.ui.misc.setText("Open Editor")

            list_of_options = []

            data = self.parent.preferences.get("DASHBOARDS", 2)
            for option in data:
                list_of_options.append(option)

            self.ui.options.addItems(list_of_options)
            self.ui.options.setCurrentText(str(current_value))
            self.ui.options.currentIndexChanged.connect(self.update_profile_config)

            self.ui.misc.clicked.connect(self.open_profile_editor)

        elif data_type == "select_theme":
            self.ui.options.show()
            list_of_options = []

            data = self.parent.preferences.get("THEMES", 4)
            for option in data:
                list_of_options.append(option)

            self.ui.options.addItems(list_of_options)
            self.ui.options.setCurrentText(str(current_value))
            self.ui.options.currentIndexChanged.connect(self.update_theme)

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
        try:
            folder_path = os.path.abspath(
                self.parent.preferences.get_preference(self.config_name)
            )

            if folder_path:
                # Open the folder in the default file explorer
                if os.name == "nt":  # Windows
                    subprocess.run(["explorer", folder_path])
                elif os.name == "posix":  # Linux/Unix
                    subprocess.run(["xdg-open", folder_path])
                else:
                    raise Exception("Unsupported operating system")

                # Save the relative path to the function or configuration (adjust as per your requirement)
                self.folder_path = os.path.relpath(folder_path)
        except Exception as e:
            raise Exception(f"Error: {e}")

    def change_folder_action(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Folder", options=options, directory="./"
        )

        if folder_path:
            self.parent.preferences.update_preference(self.config_name, folder_path)

            simplified_path = "/".join(
                folder_path.split("/")[-2:]
            )  # Get the last two folders

            if len(simplified_path) > 20:
                simplified_path = simplified_path[:18] + "..."

            self.ui.folder.setText(simplified_path)

        if self.restart:
            self.ui.restart.show()

    def update_spinbox_config(self):
        # Update the integer value in the configuration
        value = self.ui.spinBox.value()
        self.parent.preferences.update_preference(self.config_name, int(value))

        if self.restart:
            self.ui.restart.show()

    def update_text_config(self):
        # Update the string value in the configuration
        value = self.ui.string.text()
        self.parent.preferences.update_preference(self.config_name, str(value))

        if self.restart:
            self.ui.restart.show()

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

        if self.restart:
            if self.last_value == new_value:
                self.ui.restart.hide()

            else:
                self.last_value = not new_value
                self.ui.restart.show()

    def update_profile_config(self):
        # Update the selected profile in the configuration
        value = self.ui.options.currentText()
        self.parent.preferences.update_preference(self.config_name, str(value))
        self.parent.visualization_model.dashboards.switch_dashboard()

    def update_theme(self):
        value = self.ui.options.currentText()
        self.parent.preferences.update_preference(self.config_name, str(value))
        self.parent.load_theme()

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

    def google_login(self):
        self.parent.cloud_model.login()

    def google_logout(self):
        if self.parent.window_controller.show_confirm_dialog("Log Out"):
            if self.parent.recording_controller.cloud_backup_enabled:
                self.parent.recording_controller.toggle_cloud_backup()
            self.parent.cloud_model.logout()
            self.ui.profile.hide()

    def set_to_logged_in(self, is_logged_in):
        if is_logged_in:
            if not is_logged_in == "NO_INTERNET":
                self.ui.misc.setText("Log Out")

                try:
                    self.ui.misc.clicked.disconnect(self.google_login)
                except:
                    pass
                self.ui.misc.clicked.connect(self.google_logout)

                self.ui.misc.setStyleSheet(
                    """
        QPushButton{
            border-radius: 4px;
            border: 1px solid rgba(235, 77, 75,0.8);
            background-color: rgba(255, 121, 121,0.5);
            border-left: 0px;
            color: rgba(255, 255, 255, 0.65);
            font: 63 10.5pt "Video SemBd";

        }"""
                )

            else:
                self.ui.misc.setText("Try Again")

                try:
                    self.ui.misc.clicked.disconnect(self.google_logout)
                except:
                    pass
                try:
                    self.ui.misc.clicked.disconnect(self.google_login)
                except:
                    pass

                self.ui.misc.clicked.connect(self.try_again_drive)

        else:
            self.ui.misc.setText("Log In")

            try:
                self.ui.misc.clicked.disconnect(self.google_logout)
            except:
                pass

            self.ui.misc.clicked.connect(self.google_login)

            self.ui.label_config_name.setText(self.name)
            self.ui.description_label.setText(self.description)
            self.ui.description_label.setOpenExternalLinks(True)
            self.ui.misc.setStyleSheet(self.default_style)

        self.ui.misc.setEnabled(True)

    def try_again_drive(self):
        self.ui.description_label.setText(f"Loading Google Account Data...")
        self.ui.label_config_name.setText(f"Loading Google Account...")
        self.ui.misc.setText("Loading...")
        self.ui.profile.hide()
        self.ui.misc.clicked.disconnect(self.try_again_drive)
        self.parent.cloud_model.check_account()

    def update_gmail(self, gmail):
        if gmail == "NO_INTERNET":
            self.ui.description_label.setText(
                'No internet connection available, connect to the internet and hit "TRY AGAIN", cosmos will still work without internet connection.'
            )
            self.ui.label_config_name.setText("Can't Load Account")
            self.ui.misc.setText("Try Again")

            self.ui.profile.show()
            pixmap = QPixmap("./src/config/cloud/private/error.png")
            pixmap = pixmap.scaled(65, 65)
            self.ui.profile.setPixmap(pixmap)

        else:
            self.ui.description_label.setText(f"Logged in google as '{gmail}'")
            self.ui.label_config_name.setText(f"{gmail}")

            self.ui.profile.show()
            pixmap = QPixmap("./src/config/cloud/profile.jpg")
            pixmap = pixmap.scaled(65, 65)
            self.ui.profile.setPixmap(pixmap)

    def open_profile_editor(self):
        exe_path = os.path.abspath("./build/exe.win-amd64-3.11/cosmos.exe")
        if os.path.exists(exe_path):
            os.startfile(exe_path)

        else:
            self.parent.window_controller.show_error_dialog(
                "Editor Not Installed", "the editor is not installed in the system."
            )
