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
This module defines a WindowController class that manages various functionalities for the application.
"""
import random
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WindowController:
    """
    It handles toggling pages, fullscreen mode,
    dropdown animation, connection dropdown, small mode toggling, and setting visual looks. The module provides methods to interact with these features
    and also includes a function to display error dialogs.
    """

    def __init__(self, parent):
        self.parent = parent
        self.ui = parent.ui
        self.preferences = parent.preferences

        self.dropdown_enabled = True
        self.small_mode_was_toggled = None
        self.preferences_page_enabled = False
        self.missions_page_enabled = False

        self.small_mode_toggled = not self.preferences.get("HIDDEN.small_mode", 1)

        self.update_progress_bar_timer = QTimer()
        self.update_progress_bar_timer.timeout.connect(self.update_progress)

        self.progress_bar_time = 1

        self.setup_dropdown_animation()
        self.toggle_small_mode()

    # Toggle pages

    def toggle_join_room_page(self):
        self.ui.stackedWidget_3.setCurrentIndex(1)

    def toggle_preferences_page(self):
        if self.preferences_page_enabled:
            self.preferences_page_enabled = False
            self.ui.stackedWidget_central.setCurrentWidget(
                self.ui.page_centralDashboard
            )

            if self.small_mode_was_toggled:
                self.toggle_small_mode()

        else:
            self.preferences_page_enabled = True
            self.ui.stackedWidget_central.setCurrentWidget(self.ui.page_preferences)
            self.small_mode_was_toggled = self.small_mode_toggled

            if self.small_mode_toggled:
                self.toggle_small_mode()

    def toggle_mission_page(self):
        self.missions_page_enabled = not self.missions_page_enabled

        if self.missions_page_enabled:
            self.ui.StackedWidget_mainSidebar.setCurrentIndex(1)

        else:
            self.ui.StackedWidget_mainSidebar.setCurrentIndex(0)

    # Toggle fullscreen
    def toggle_fullscreen(self):
        if self.parent.isFullScreen():
            self.parent.showNormal()

            self.parent.titleBar.show()
            self.parent.ui.topbarseparator.setMaximumHeight(34)
            self.parent.ui.topbarseparator.setMinimumHeight(34)

            self.parent.ui.btn_smallModeTogle.show()

        else:
            self.parent.showFullScreen()
            self.parent.titleBar.hide()
            self.parent.ui.btn_smallModeTogle.hide()

            self.parent.ui.topbarseparator.setMaximumHeight(15)
            self.parent.ui.topbarseparator.setMinimumHeight(15)

    # Dropdown
    def setup_dropdown_animation(self):
        # Animation for showing the dropdown menu
        self.animation_dropdown_on = QPropertyAnimation(
            self.ui.frame_connectionDropDown, b"maximumHeight"
        )
        self.animation_dropdown_on.setDuration(95)
        self.animation_dropdown_on.setStartValue(0)
        self.animation_dropdown_on.setEndValue(70)
        self.animation_dropdown_on.setEasingCurve(QEasingCurve.OutQuad)

        # Animation for hiding the dropdown menu
        self.animation_dropdown_off = QPropertyAnimation(
            self.ui.frame_connectionDropDown, b"maximumHeight"
        )
        self.animation_dropdown_off.setDuration(95)
        self.animation_dropdown_off.setStartValue(70)
        self.animation_dropdown_off.setEndValue(0)
        self.animation_dropdown_off.setEasingCurve(QEasingCurve.OutQuad)

        self.animation_dropdown_off.start()
        self.animation_dropdown_on.start()

    def toggle_connection_dropdown(self):
        if self.dropdown_enabled:
            self.dropdown_enabled = False
            self.animation_dropdown_off.start()

        else:
            self.dropdown_enabled = True
            self.animation_dropdown_on.start()

    # Toggle Small Mode
    def toggle_small_mode(self):
        if self.small_mode_toggled:
            self.preferences.update("HIDDEN.small_mode", False, 1)

            self.ui.frame_dsahboardGraph.show()

            self.parent.setMinimumWidth(750)
            self.parent.setMaximumWidth(16777215)
            self.parent.resize(QSize(1150, self.parent.height()))

            self.ui.btn_smallModeTogle.setChecked(False)

        else:
            self.preferences.update("HIDDEN.small_mode", True, 1)

            self.ui.frame_dsahboardGraph.hide()

            self.parent.setMinimumWidth(273)
            self.parent.setMaximumWidth(273)
            self.parent.resize(QSize(273, self.parent.height()))
            self.ui.btn_smallModeTogle.setChecked(True)

        self.small_mode_toggled = not self.small_mode_toggled

    # Set Looks
    def set_default_look(self):
        self.ui.btn_connectBtn.setChecked(False)
        self.ui.btn_connectBtn.setText("CONNECT")

    def set_connected_look(self, port):
        self.ui.btn_connectBtn.setChecked(True)
        self.ui.btn_connectBtn.setText(f"CONNECTED: [ {port} ]")

    def start_progress_bar(self):
        self.ui.progress_bar_statusBar.show()
        self.ui.progress_bar_statusBar.setValue(0)

        # Start the timer with a 10 millisecond interval
        self.update_progress_bar_timer.start(self.progress_bar_time)

    def stop_progress_bar(self):
        self.ui.progress_bar_statusBar.setValue(100)
        self.ui.progress_bar_statusBar.hide()
        self.progress_bar_time = 1

    def update_progress(self):
        if self.ui.progress_bar_statusBar.value() > 80:
            self.progress_bar_time += 10

        else:
            new_value = self.ui.progress_bar_statusBar.value() + 5
            self.ui.progress_bar_statusBar.setValue(new_value)

        self.update_progress_bar_timer.setInterval(self.progress_bar_time)
        # Get the current value of the progress bar
        current_value = self.ui.progress_bar_statusBar.value()

        # If the value is less than 99, add 1
        if current_value < 99:
            self.ui.progress_bar_statusBar.setValue(current_value + 1)
        else:
            # If 99 is reached, stop the timer
            self.update_progress_bar_timer.stop()

    def setTitle(self, title):
        if title:
            self.parent.setWindowTitle(f"{self.parent.name.upper()} - {title}")

        else:
            self.parent.setWindowTitle(self.parent.name.upper())

    # Show Error Dialog
    def show_error_dialog(self, title, error_message):
        self.msg = QMessageBox()
        self.msg.setWindowTitle(f"Cosmos Runtime Error: {title}")
        self.msg.setText(f"Error: {error_message}")
        self.msg.setIcon(QMessageBox.Critical)

        close_btn = self.msg.addButton("Close", QMessageBox.AcceptRole)
        self.msg.setWindowIcon(QIcon("./src/ui/resources/app.ico"))

        self.msg.setDefaultButton(close_btn)

        self.msg.exec_()

    def show_info_dialog(self, title, info_msg):
        self.msg = QMessageBox()
        self.msg.setWindowTitle(title)
        self.msg.setText(info_msg)
        self.msg.setIcon(QMessageBox.Information)  # Corrected this line

        close_btn = self.msg.addButton("Close", QMessageBox.AcceptRole)
        self.msg.setWindowIcon(QIcon("./src/ui/resources/app.ico"))
        self.msg.setDefaultButton(close_btn)
        self.msg.exec_()

    def show_confirm_dialog(self, title):
        self.msg = QMessageBox()
        self.msg.setWindowTitle(f"Continue with {title}")
        self.msg.setText(f"Are you sure you want to continue with {title} ?")
        self.msg.setIcon(QMessageBox.Question)
        self.msg.setWindowIcon(QIcon("./src/ui/resources/app.ico"))

        continue_btn = self.msg.addButton("Continue", QMessageBox.AcceptRole)
        go_back_btn = self.msg.addButton("Go Back", QMessageBox.RejectRole)

        self.msg.setDefaultButton(continue_btn)

        self.msg.exec_()

        if self.msg.clickedButton() == go_back_btn:
            return False
        elif self.msg.clickedButton() == continue_btn:
            return True
