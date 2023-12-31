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
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPainter

from ..visualization.dashboards import DashboardsModel
from .information_updater import InformationUpdateModel


class VisualizationModel(QObject):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.ui = parent.ui
        self.preferences = parent.preferences

        self.graph_layout = None
        self.setup_pyqtgraph()

        self.dashboards = DashboardsModel(self)
        self.updates = InformationUpdateModel(self)

        self.text_color = "rgb(240,240,240)"

    def change_to_connected(self):
        self.updates.widget_update_timer.start()
        self.updates.data_stale_timer.start()
        self.parent.terminal_controller.terminal_clearer.start()

    def change_to_disconnected(self):
        self.updates.widget_update_timer.stop()
        self.updates.data_stale_timer.stop()
        self.parent.terminal_controller.terminal_clearer.stop()

        self.updates.previus_state = None
        self.updates.current_state = None
        self.updates.value_chain = np.asarray(["default"])

        self.set_state("N/A", "45484e")
        self.updates.clear_labels()
        self.updates.clear_graphs()

    def set_state(self, name, color):
        # Set the background color, border, and text color of the state label
        self.ui.label_state.setStyleSheet(
            f"""
                background-color: #4D{color};
                border: 1.5px solid #{color};
                color: {self.text_color};"""
        )

        # Set the text of the state label
        self.ui.label_state.setText(name)

    def setup_pyqtgraph(self):
        pg.setConfigOptions(
            background=(14, 16, 20, 0),
            foreground=(195, 195, 195),
            segmentedLineMode="on",
            exitCleanup=True,
            antialias=self.parent.preferences.get_preference(
                "advanced.graphs_antialias"
            ),
            useOpenGL=self.parent.preferences.get_preference("advanced.opengl_enabled"),
            useCupy=True,
            useNumba=True,
        )

        main_layout = pg.GraphicsLayoutWidget()
        main_layout.setAntialiasing(False)
        main_layout.setRenderHints(QPainter.Antialiasing)

        self.graph_layout = main_layout.addLayout(
            colspan=1, rowspan=1, border=(0, 0, 0, 0)
        )
        self.graph_layout.setContentsMargins(0, 0, 0, 0)
        self.graph_layout.setSpacing(0)

        self.parent.ui.layout_graphContainer.addWidget(main_layout)

    def update_colors(self, text_color, background_color2):
        self.text_color = text_color
        pg.setConfigOptions(
            foreground=text_color,
        )
        self.dashboards.switch_dashboard()
        self.updates.update_graphs_color(text_color)
        self.set_state("N/A", background_color2.replace("#", ""))
