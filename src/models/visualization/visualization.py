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

from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QObject

import pyqtgraph as pg

from ..visualization.dashboards import DashboardsModel


class VisualizationModel(QObject):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.preferences = parent.preferences

        self.graph_layout = None
        self.setup_pyqtgraph()
        
        self.dashboars_model = DashboardsModel(self)

    def setup_pyqtgraph(self):
        pg.setConfigOptions(
            background=(14, 16, 20, 0),
            foreground=(195, 195, 195, 0),
            segmentedLineMode="off",
            exitCleanup=True,
            antialias=True,
            useOpenGL=False,
            useCupy=True,
            useNumba=True,
        )

        main_layout = pg.GraphicsLayoutWidget()
        main_layout.setAntialiasing(True)
        main_layout.setRenderHints(QPainter.Antialiasing)

        self.graph_layout = main_layout.addLayout(colspan=1, rowspan=1, border=(4, 4, 4, 4))
        self.graph_layout.setContentsMargins(1, 1, 1, 1)
        self.graph_layout.setSpacing(4)

        self.parent.ui.layout_graphContainer.addWidget(main_layout)
