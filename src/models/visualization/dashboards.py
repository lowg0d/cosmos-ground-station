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
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton

from ..visualization.plot_widgets import (
    DualAxePlotWidget,
    GpsPlotWidget,
    MonoAxePlotWidget,
    TripleAxePlotWidget,
)


class DashboardsModel(QObject):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.ui = self.parent.parent.ui
        self.preferences = parent.preferences

        # layouts for the widgets
        self.button_container = self.ui.layout_buttonContainer
        self.big_label_container = self.ui.layout_BigTlmLabels
        self.primary_label_container = self.ui.layout_PrimaryTlmLabel
        self.secondary_label_container = self.ui.layout_SecondaryTlmLabelContainer
        self.graph_container_layout = self.parent.graph_layout

        self.current_profile = None
        self.current_buttons_data = None
        self.current_states_data = None
        self.current_labels_data = None
        self.current_graphs_data = None
        self.current_max_columns = None

        self.states_map = None
        self.filter_ranges_map = None
        self.labels_map = {}
        self.buttons_map = {}
        self.mono_axe_map = {}
        self.dual_axe_map = {}
        self.triple_axe_map = {}
        self.gps_map = {}

        self.pen_width = None
        self.graph_data_points = None
        self.gps_graph_data_points = None

        self.setup_current()

    def setup_current(self):
        self.current_profile = self.preferences.get_preference(
            "dashboard.visualization_dashboard"
        )

        exits = self.preferences.get(
            f"DASHBOARDS.{self.current_profile}", 2, not_exit=True
        )

        if exits == "NotFound":
            dash_list = self.preferences.get("DASHBOARDS", 2)
            dash_list = list(dash_list.keys())  # Convert dict_keys to a list
            if len(dash_list) > 0:
                self.preferences.update_preference(
                    "dashboard.visualization_dashboard", dash_list[0]
                )
                self.parent.parent.notifications.new(
                    msg=f"Dashboard '{self.current_profile}' Not Found, changed to '{dash_list[0]}'",
                    level="warning",
                    duration="long",
                )
                self.current_profile = dash_list[0]

            else:
                exit("[ERROR] NO DASHBOARD FILE DETECTED")

        self.update_profile_data()
        self.update_ui_widgets()

    def destroy_current(self):
        self.destroy_widgets_from_layout(self.button_container)
        self.destroy_widgets_from_layout(self.big_label_container)
        self.destroy_widgets_from_layout(self.primary_label_container)
        self.destroy_widgets_from_layout(self.secondary_label_container)
        self.graph_container_layout.clear()

        self.current_profile = None
        self.current_buttons_data = None
        self.current_states_data = None
        self.current_labels_data = None
        self.current_graphs_data = None
        self.current_max_columns = None

        self.states_map = None
        self.filter_ranges_map = None
        self.labels_map = {}
        self.buttons_map = {}
        self.mono_axe_map = {}
        self.dual_axe_map = {}
        self.triple_axe_map = {}
        self.gps_map = {}

        self.pen_width = None
        self.graph_data_points = None
        self.gps_graph_data_points = None

    def update_ui_widgets(self):
        try:
            self.setup_graphs()
            self.setup_buttons()
            self.setup_labels()

        except Exception as e:
            exit(f"[CRITICAL] Unknown error loading dashboard: {e}")

    def switch_dashboard(self):
        self.destroy_current()
        self.setup_current()

    def update_profile_data(self):
        data = self.preferences.get(f"DASHBOARDS.{self.current_profile}", 2)
        self.current_max_columns = data["max_columns"]
        self.pen_width = data["graph_pen_width"]
        self.graph_data_points = data["graph_data_points"]
        self.gps_graph_data_points = data["gps_graph_data_points"]

        self.states_map = self.preferences.get(f"STATES.{data['states']}", 2)
        self.filter_ranges_map = self.preferences.get(
            f"FILTER_RANGES.{data['filter_ranges']}", 2
        )
        self.current_buttons_data = self.preferences.get(
            f"BUTTONS.{data['buttons']}", 2
        )
        self.current_labels_data = self.preferences.get(f"LABELS.{data['labels']}", 2)
        self.current_graphs_data = self.preferences.get(f"GRAPHS.{data['graphs']}", 2)

    ############################################################
    ## BUTTONS
    ############################################################
    def setup_buttons(self):
        amount = len(self.current_buttons_data)

        if amount > 0:
            rows = self.calculate_rows(amount)
            current_row, current_column = 0, 0

            for data in self.current_buttons_data:
                widget = self.generate_button(data)

                self.button_container.addWidget(widget, current_row, current_column)

                current_row += 1
                if current_row >= rows:
                    current_row = 0
                    current_column += 1

    def generate_button(self, data):
        name = data["name"]
        color = data["color"]
        payload = data["payload"]
        button_widget = QPushButton(parent=self.parent.parent, text=name)

        button_widget.clicked.connect(self.cmd_button_click)

        button_widget.setMinimumHeight(30)
        button_widget.setMaximumHeight(30)
        button_widget.setObjectName(name.replace(" ", "_"))
        button_widget.setCursor(QCursor(Qt.PointingHandCursor))

        button_widget.setStyleSheet(
            "QPushButton {"
            + f"""
                    background-color: #4D{color};
                    font: 500 9pt "Video Med";
                    border-radius: 4px;
                    border: 2px solid #{color};
                """
            "}"
            + """
                QPushButton:hover {"""
            + f"""
                    border: 2px solid #99{color};
                    background-color: #33{color};
                """
            "}"
            + """
                QPushButton:pressed {"""
            + f"""
                    border: 2px solid #E6{color};
                    background-color: #E6{color};
                """
            "}"
        )

        self.buttons_map[button_widget] = payload
        return button_widget

    def cmd_button_click(self, sender):
        button = self.sender()
        cmd = self.buttons_map[button]
        self.parent.parent.connection_controller.send_data_action(cmd)

    ############################################################
    ## LABELS
    ############################################################
    def setup_labels(self):
        big = self.current_labels_data["big"]
        big_amount = len(big)

        primary = self.current_labels_data["primary"]
        primary_amount = len(primary)

        secondary = self.current_labels_data["secondary"]
        secondary_amount = len(secondary)

        ## Generate Big Labels
        if big_amount > 0:
            self.generate_type_labels(type_="big", data=big, amount=big_amount)

        if primary_amount > 0:
            self.generate_type_labels("primary", primary, primary_amount)

        if secondary_amount > 0:
            self.generate_type_labels("secondary", secondary, secondary_amount)

    def generate_type_labels(self, type_: str, data, amount):
        if type_ == "big":
            layout = self.big_label_container
            labels_data = self.current_labels_data["big"]

        elif type_ == "primary":
            layout = self.primary_label_container
            labels_data = self.current_labels_data["primary"]

        elif type_ == "secondary":
            layout = self.secondary_label_container
            labels_data = self.current_labels_data["secondary"]

        rows = self.calculate_rows(amount)
        current_row, current_column = 0, 0

        for data in labels_data:
            widget = self.generate_label(data)

            layout.addLayout(widget, current_row, current_column)

            current_row += 1
            if current_row >= rows:
                current_row = 0
                current_column += 1

    def generate_label(self, data):
        name = data["name"]

        if len(name) > 10:
            name = name[:7] + "..."
        else:
            name = name

        unit = data["unit"]
        value_index = data["value_index_in_chain"]
        min_max = data.get("min_max_nomial")

        default_value = "N/A"

        if unit:
            show_unit = True

        else:
            show_unit = False

        if unit == "format_seconds":
            default_value = "00:00:00"
            unit_to_print = ""
            show_unit = False
        elif unit == "tlm_rate":
            unit_to_print = " ms"
        elif unit == "sensor":
            unit_to_print = ""
        else:
            unit_to_print = f"{unit}"

        if min_max != None:
            name_label = QLabel(f"{name}<b>:</b>  ")

        else:
            name_label = QLabel(f""" {name}<b>:</b>  """)

        unit_label = QLabel(f" {unit_to_print}")
        tlm_label = QLabel(f"""<b>{default_value}</b>""")

        group_layout = QHBoxLayout()

        group_layout.addWidget(name_label, alignment=Qt.AlignLeft)
        group_layout.addStretch(1)
        group_layout.addWidget(tlm_label, alignment=Qt.AlignRight)

        if show_unit:
            group_layout.addWidget(unit_label, alignment=Qt.AlignRight)

        group_layout.addSpacing(10)

        self.labels_map[tlm_label] = (value_index, unit)
        return group_layout

    ############################################################
    ## GRAPHS
    ############################################################
    def setup_graphs(self):
        amount = len(self.current_graphs_data)

        if amount > 0:
            for data in self.current_graphs_data:
                widget = self.generate_graph(data)
                row = data["row"]
                col = data["col"]

                self.graph_container_layout.addItem(widget, row, col)

    def generate_graph(self, data):
        axes = data.get("axes")
        name = data.get("title")
        unit = data.get("unit")
        color_1 = data.get("color_1")
        value_index = data.get("value_index_in_chain_1")

        if axes == 1:
            graph_widget = MonoAxePlotWidget(
                title=f"{name} ({unit})",
                name=name,
                color=color_1,
                pen_width=self.pen_width,
                datapoints=self.graph_data_points,
            )

            self.mono_axe_map[graph_widget] = value_index
            graph_widget.update(0.0)

        elif axes == 2:
            value_index_2 = data.get("value_index_in_chain_2")

            graph_widget = DualAxePlotWidget(
                title=f"{name} ({unit})",
                name_1=data.get("name_1"),
                name_2=data.get("name_2"),
                color_1=color_1,
                color_2=data.get("color_2"),
                pen_width=self.pen_width,
                datapoints=self.graph_data_points,
            )
            self.dual_axe_map[graph_widget] = (value_index, value_index_2)
            graph_widget.update(0.0, 0.0)

        elif axes == 3:
            value_index_2 = data.get("value_index_in_chain_2")
            value_index_3 = data.get("value_index_in_chain_3")

            graph_widget = TripleAxePlotWidget(
                title=f"{name} ({unit})",
                name_1=data.get("name_1"),
                name_2=data.get("name_2"),
                name_3=data.get("name_3"),
                color_1=color_1,
                color_2=data.get("color_2"),
                color_3=data.get("color_3"),
                pen_width=self.pen_width,
                datapoints=self.graph_data_points,
            )

            self.triple_axe_map[graph_widget] = (
                value_index,
                value_index_2,
                value_index_3,
            )

            graph_widget.update(0.0, 0.0, 0.0)

        elif axes.lower() == "gps":
            value_index_2 = data.get("value_index_in_chain_2")
            graph_widget = GpsPlotWidget(
                title=f"{name} ({unit})",
                color=color_1,
                datapoints=self.gps_graph_data_points,
            )
            self.gps_map[graph_widget] = (value_index, value_index_2)
            graph_widget.update(0.0, 0.0)

        return graph_widget

    ############################################################
    ## MISC
    ############################################################
    # calculate the row amount for X columns
    def calculate_rows(self, amount):
        # calculate the maximum number of items per column based on 1.5 items per row.
        max_per_column = int(round(amount / 3.5))

        # ensure there's at least one item per column, even if the amount is small.
        # also, limit the number of columns to a maximum of 2.
        num_columns = min(
            (amount + max_per_column - 1) // max_per_column, self.current_max_columns
        )

        # calculate the number of rows based on the number of columns.
        num_rows = (amount + num_columns - 1) // num_columns

        # return the calculated number of rows.
        return num_rows

    def destroy_widgets_from_layout(self, layout):
        if isinstance(layout, QGridLayout):
            # Clear the layout's columns and rows
            for i in reversed(range(layout.columnCount())):
                layout.setColumnMinimumWidth(i, 0)
                layout.setColumnStretch(i, 0)

            for i in reversed(range(layout.rowCount())):
                layout.setRowMinimumHeight(i, 0)
                layout.setRowStretch(i, 0)

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout is not None:
                    self.destroy_widgets_from_layout(sub_layout)
