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
import time
from collections import deque

import numpy as np
from PyQt5.QtCore import QDateTime, QObject, QTimer


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

        self.data_stale_enabled = True
        self.previous_state = None
        self.previous_value_chain = np.asarray([])
        self.value_chain = np.asarray(["default"])
        self.smoothed_values = []  # Initialize with an empty list for smoothed values

        self.label_index_error = False

        self.plotting_times = deque(maxlen=500)
        self.filter_times = deque(maxlen=500)

        self.last_update_time = QDateTime.currentDateTime()
        self.tlm_delta = 0

        self.widget_update_timer = QTimer()
        self.widget_update_timer.setInterval(self.update_interval)
        self.widget_update_timer.timeout.connect(self.update_all_widgets)

        self.data_stale_timer = QTimer()
        self.data_stale_timer.setInterval(500)
        self.data_stale_timer.timeout.connect(self.handle_data_stale)

    def update_value_chain(self, new_values):
        # update the value chain with the new values, and record the time for calculating the tlm rate
        now = QDateTime.currentDateTime()

        # update the last_updated_time to the current time, and calculate the tlm rate
        self.tlm_delta = self.last_update_time.msecsTo(now)
        self.last_update_time = now

        self.value_chain = np.asarray(new_values)

        # filter the data is filter is enabled
        if self.preferences.get_preference("data.data_filter"):
            try:
                # start_time = time.time()

                self.handle_data_filtration()

                # plotting_time = (time.time() - start_time) * 1000
                # self.filter_times.append(plotting_time)
                # print(
                #    f"\rFILTER TIME: {round(sum(self.filter_times) / len(self.filter_times), 2)} ms SAMPLES: {len(self.filter_times)}/{self.filter_times.maxlen}",
                #    end="",
                #    flush=True,
                # )

            except:
                return

    def update_all_widgets(self):
        start_time = time.time()

        try:
            self.update_labels()
            self.update_state()
            self.update_graphs()

        except ValueError as e:
            if self.value_chain == np.asarray(["default"]):
                self.parent.set_state("WAITING FOR DATA...", "f7f1e3")
                self.last_update_time = QDateTime.currentDateTime()

            else:
                print(
                    f"[-] Error updating All Values: value is to high fo the list - {e}"
                )

        except Exception as e:
            print(f"[-] Error Updating All Widgets: {e}")

        plotting_time = (time.time() - start_time) * 1000
        self.plotting_times.append(plotting_time)
        print(
            f"\rPLOT TIME: {round(sum(self.plotting_times) / len(self.plotting_times), 2)} ms SAMPLES: {len(self.plotting_times)}/{self.plotting_times.maxlen}",
            end="",
            flush=True,
        )

    ############################################################
    ## HANDLERS
    ############################################################
    def handle_data_stale(self):
        current_time = QDateTime.currentDateTime()
        elapsed = self.last_update_time.msecsTo(current_time)

        if (elapsed / 1000) > self.data_stale_detect_time:
            if not self.data_stale_enabled:
                self.data_stale_enabled = True
                self.widget_update_timer.setInterval((self.update_interval * 4))
                self.data_stale_timer.setInterval(50)
                formatted_time = current_time.toString("yyyy-MM-dd hh:mm:ss.zzz")
                # Print the formatted time
                print(f"[{formatted_time}]: DATA STALE MODE ENABLED !!")
                self.parent.parent.terminal_controller.terminal_clearer.stop()

            seconds = elapsed / 1000
            self.parent.set_state(f"DATA STALE [{seconds:.1f}s]", "f7f1e3")

        else:
            if self.data_stale_enabled:
                self.data_stale_enabled = False
                self.previous_state = None

                self.widget_update_timer.setInterval(self.update_interval)
                self.data_stale_timer.setInterval(1000)
                self.parent.parent.terminal_controller.terminal_clearer.start()

    def handle_data_filtration(self):
        filtered_values = []
        for i, old_value in enumerate(self.value_chain):
            old_value = float(old_value)
            if str(i) in self.dashboards.filter_ranges_map:
                min_val, max_val = self.dashboards.filter_ranges_map[str(i)]
                if old_value < min_val:
                    new_value = min_val

                elif old_value > max_val:
                    new_value = max_val

                else:
                    new_value = old_value

                filtered_values.append(new_value)

            else:
                filtered_values.append(old_value)
                print(
                    f"[WARNING] (INDEX: {i}) Data Filtration is activated but you are not providing values to filter."
                )

        self.value_chain = np.asarray(filtered_values)

    ############################################################
    ## GRAPHS
    ############################################################
    def update_graphs(self):
        ## MONO
        try:
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
        except IndexError:
            if not self.label_index_error:
                if np.all(self.value_chain == "default"):
                    pass
                else:
                    self.label_index_error = not self.label_index_error
                    self.parent.parent.notifications.new(
                        msg="(GRAPHS) Value Expected But Not <b>RECEIVED</b>, Check Dashboards.json",
                        level="error",
                        duration="permanent",
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

    def update_graphs_color(self, text_color):
        ## MONO
        for widget, value_index in self.dashboards.mono_axe_map.items():
            widget.change_color(text_color)

        ## DUAl
        for widget, (
            value_index,
            value_index_2,
        ) in self.dashboards.dual_axe_map.items():
            widget.change_color(text_color)

        ## TRIPLE
        for widget, (
            value_index,
            value_index_2,
            value_index_3,
        ) in self.dashboards.triple_axe_map.items():
            widget.change_color(text_color)

        ## GPS
        for widget, (
            value_index,
            value_index_2,
        ) in self.dashboards.gps_map.items():
            widget.change_color(text_color)

    ############################################################
    ## STATES
    ############################################################
    def update_state(self):
        current_state = int(self.value_chain[self.state_index])

        if current_state != self.previous_state:
            self.previous_state = current_state

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
        try:
            for label, (value_index, unit) in self.dashboards.labels_map.items():
                # check for especial cases like tlm_rate or convert to time
                if unit == "tlm_rate":
                    plot_value = self.tlm_delta

                elif unit == "format_seconds":
                    plot_value = self.format_time(float(self.value_chain[value_index]))

                elif unit == "sensor":
                    value = self.value_chain[value_index]
                    if value == 0:
                        plot_value = "OFF"

                    elif value == 1:
                        plot_value = "ON"

                else:
                    plot_value = float(self.value_chain[value_index])
                    plot_value = (
                        int(plot_value)
                        if plot_value.is_integer()
                        else round(plot_value, 4)
                    )

                # set the label's text with the updated value_to_plot
                label.setText(f"<b>{plot_value}</b>")
        except IndexError:
            if not self.label_index_error:
                if np.all(self.value_chain == "default"):
                    pass
                else:
                    self.label_index_error = not self.label_index_error
                    self.parent.parent.notifications.new(
                        msg="(LABELS) Value Expected But Not <b>RECEIVED</b>, Check Dashboards.json",
                        level="error",
                        duration="permanent",
                    )

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
