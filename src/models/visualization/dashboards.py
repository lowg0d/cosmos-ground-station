######################### Xnxe9 <3? #########################
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

from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout

from ..visualization.plot_widgets import (
    MonoAxePlotWidget,
    DualAxePlotWidget,
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
        self.telemetry_labels_map = {}
        self.buttons_map = {}
        self.mono_axe_map = {}
        self.dual_axe_map = {}
        self.tri_axe_map = {}
        self.gps_map = {}

        self.setup_current()

    def setup_current(self):
        self.current_profile = self.preferences.get_preference(
            "profiles.visualization_dashboard"
        )

        self.update_profile_data()
        self.update_ui_widgets()

    def update_ui_widgets(self):
        try:
            self.setup_buttons()
            self.setup_labels()
            self.setup_graphs()

        except Exception as e:
            exit(f"[CRITICAL] Unknown error loading dashboard: {e}")

    def update_profile_data(self):
        data = self.preferences.get(f"DASHBOARDS.{self.current_profile}", 2)
        self.current_max_columns = data["max_columns"]

        self.current_states_data = self.preferences.get(f"STATES.{data['states']}", 2)
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
                    color: rgba(255, 255, 255, 0.9);
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
        unit = data["unit"]
        value_index = data["value_index_in_chain"]

        try:
            min_max = data["min_max_nomial"]

        except:
            min_max = None

        default_value = "N/A"

        if unit == "format_seconds":
            tbd_value = "00:00:00"
            unit_to_print = ""
        elif unit == "tlm_rate":
            unit_to_print = " ms"
        else:
            unit_to_print = f"{unit}"

        if min_max != None:
            name_label = QLabel(
                f"""<span style="color: gray; font-size: 14px">&#9679;</span> {name}<b>:</b>  """
            )

        else:
            name_label = QLabel(f""" {name}<b>:</b>  """)

        unit_label = QLabel(f" {unit_to_print}")
        tlm_label = QLabel(f"<b>{default_value}</b>")

        group_layout = QHBoxLayout()

        group_layout.addWidget(name_label, alignment=Qt.AlignLeft)
        group_layout.addStretch(1)
        group_layout.addWidget(tlm_label, alignment=Qt.AlignRight)
        group_layout.addWidget(unit_label, alignment=Qt.AlignRight)

        group_layout.addSpacing(10)

        self.telemetry_labels_map[tlm_label] = (value_index, unit)
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

    def generate_graph(seld, data):
        axes = data["axes"]
        name = data["title"]
        unit = data["unit"]
        color_1 = ["color_1"]
        value_index = data["value_index_in_chain_1"]

        if axes == 1:
            graph_widget = MonoAxePlotWidget(
                tittle=f"{name} ({unit})",
                name=name,
                color=color_1,
                color_1=["axe_color_1"],
            )

        elif axes == 2:
            value_index_2 = data["value_index_in_chain_2"]

            graph_widget = DualAxePlotWidget(
                tittle=f"{name} ({unit})",
                name_x=name,
                name_y=data["name_2"],
                color_x=color_1,
                color_x=data["color_2"],
            )

        elif axes == 3:
            value_index_2 = data["value_index_in_chain_3"]

            graph_widget = TripleAxePlotWidget()

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
