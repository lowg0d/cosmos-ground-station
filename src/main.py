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

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qframelesswindow import FramelessMainWindow

from src.ui import Ui_MainWindow, CustomTitleBar


class MainWindow(FramelessMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Set a custom title bar for the window
        self.setTitleBar(CustomTitleBar(self))

        # Setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # get the application information
        self.name = "cosmos"
        self.version = "1.0.0"
        self.dev_phase = "alpha"
        self.author = "Martin Ortiz"

        # set up window properties
        self.setWindowIcon(QIcon("./src/ui/resources/app.ico"))
        self.setWindowTitle(self.name.upper())

        # update the labels that display the info of the application
        self.ui.label_statusBar.setText(f"{self.name.lower()}-v{self.version}-{self.dev_phase}")

        # change the current apparence
        self.ui.stackedWidget_central.setCurrentWidget(self.ui.page_centralDashboard)

        self.titleBar.raise_()
        self.showMaximized()
        self.show()
