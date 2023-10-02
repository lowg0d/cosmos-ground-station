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

from PyQt5.QtCore import QObject, QDateTime, QTimer

import time
import numpy as np


class InformationUpdateModel(QObject):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.preferences = parent.preferences
        self.dashboards = parent.dashboards

        self.update_interval = self.preferences.get_preference("data.update_interval")
        self.data_stale_detect_time = self.preferences.get_preference(
            "data.data_stale_detect_time"
        )
        self.data_filter_enabled = self.preferences.get_preference("data.data_filter")
        self.state_index = self.preferences.get_preference("packet.state_value_index")

        self.previus_state = None
        self.previus_value_chain = np.asarray([])
        self.value_chain = np.asarray(["default"])

        self.last_update_time = QDateTime.currentDateTime()
        self.tlm_delta = 0

        self.widget_update_timer = QTimer()
        self.widget_update_timer.setInterval(self.update_interval)
        self.widget_update_timer.timeout.connect(self.update_all_widgets)

    def update_value_chain(self, new_values):
        # update the value chain with the new values, and record the time for calculating the tlm rate
        now = QDateTime.currentDateTime()

        # update the last_updated_time to the current time, and calculate the tlm rate
        self.tlm_delta = self.last_update_time.msecsTo(now)
        self.last_update_time = now

        self.value_chain = np.asarray(new_values)
        """
        # filter the data is filter is enabled
        if self.filter_enabled == True:
            try:
                self.data_filter()
            except:
                return
        """

    def update_all_widgets(self):
        start_time = time.time()

        try:
            self.update_graphs()
            self.update_labels()
            self.update_state()

        except IndexError as e:
            if self.value_chain == np.asarray(["default"]):
                self.parent.set_state("WAITING FOR DATA...", "f7f1e3")

            else:
                print(f"[-] Error updating All Values: value is to high fo the list - {e}")

        except Exception as e:
            print(f"[-] Error Updating All Widgets: {e}")

        plotting_time = (time.time() - start_time) * 1000
        #print(plotting_time)

    ############################################################
    ## GRAPHS
    ############################################################
    def update_graphs(self):
        ## MONO
        for widget, value_index in self.dashboards.mono_axe_map.items():
            widget.update(self.value_chain[value_index])

        ## DUAl
        for widget, (
            value_index,
            value_index_2,
        ) in self.dashboards.dual_axe_map.items():
            widget.update(
                self.value_chain[value_index], self.value_chain[value_index_2]
            )

        ## TRIPLE
        for widget, (
            value_index,
            value_index_2,
            value_index_3,
        ) in self.dashboards.triple_axe_map.items():
            widget.update(
                self.value_chain[value_index],
                self.value_chain[value_index_2],
                self.value_chain[value_index_3],
            )

        ## GPS
        for widget, (
            value_index,
            value_index_2,
        ) in self.dashboards.gps_map.items():
            widget.update(
                self.value_chain[value_index],
                self.value_chain[value_index_2],
            )

    def clear_graphs(self):
        ## MONO
        for widget, value_index in self.dashboards.mono_axe_map.items():
            widget.clear()

        ## DUAl
        for widget, (
            value_index,
            value_index_2,
        ) in self.dashboards.dual_axe_map.items():
            widget.clear()

        ## TRIPLE
        for widget, (
            value_index,
            value_index_2,
            value_index_3,
        ) in self.dashboards.triple_axe_map.items():
            widget.clear()

        ## GPS
        for widget, (
            value_index,
            value_index_2,
        ) in self.dashboards.gps_map.items():
            widget.clear()

    ############################################################
    ## STATES
    ############################################################
    def update_state(self):
        current_state = self.value_chain[self.state_index]

        if current_state != self.previus_state:
            self.previus_state = current_state

            try:
                state_data = self.dashboards.states_map.get(f"{current_state}")

                if state_data == None:
                    self.handle_invalid_state(current_state)
                    return

                name, color = state_data
                self.parent.set_state(name, color)

            except:
                self.handle_invalid_state(current_state)

    def handle_invalid_state(self, state):
        # if an exception occurs while processing the state data, handle the invalid state
        # set the previous state to None to indicate an invalid state
        self.previous_state = None

        self.parent.set_state(f"INVALID STATE: {state}", "b33939")

    ############################################################
    ## LABELS
    ############################################################
    def update_labels(self):
        for label, (value_index, unit) in self.dashboards.labels_map.items():
            # check for especial cases like tlm_rate or convert to time
            if unit == "tlm_rate":
                plot_value = self.tlm_delta

            elif unit == "format_seconds":
                plot_value = self.format_time(float(self.value_chain[value_index]))

            else:
                plot_value = float(self.value_chain[value_index])

            # set the label's text with the updated value_to_plot
            label.setText(f"<b>{plot_value}</b>")

    def format_time(self, time_in_seconds):
        # format the time in seconds to a human-readable time format (hh:mm:ss)
        hours, remainder = divmod(time_in_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"


    def clear_labels(self):
        for label, (value_index, unit) in self.dashboards.labels_map.items():
            if unit == "format_seconds":
                plot_value = "00:00:00"

            else:
                plot_value = "N/A"

            # set the label's text with the updated value_to_plot
            label.setText(f"<b>{plot_value}</b>")