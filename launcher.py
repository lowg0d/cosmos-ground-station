######################### Xnxe9 <3? #########################
#
#   .o88b.  .d88b.  .d8888. .88b  d88.  .d88b.  .d8888.
#  d8P  Y8 .8P  Y8. 88'  YP 88'YbdP`88 .8P  Y8. 88'  YP
#  8P      88    88 `8bo.   88  88  88 88    88 `8bo.
#  8b      88    88   `Y8b. 88  88  88 88    88   `Y8b.
#  Y8b  d8 `8b  d8' db   8D 88  88  88 `8b  d8' db   8D
#   `Y88P'  `Y88P'  `8888Y' YP  YP  YP  `Y88P'  `8888Y'
#
# ★ StarLab RPL ★ - COSMOS GROUND STATION
# Communications and Observation Station for Mission Operations and Surveillance
#
# By Martin Ortiz
# Version 1.0.0
# Date 06.08.2023
#
#############################################################
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from src import MainWindow

def fix_dpi():
    """
    fix scale and high DPI issues for the application.
    """
    # set environment variable to adjust DPI for font rendering
    os.environ["QT_FONT_DPI"] = "96"

    # set high DPI scaling factor rounding policy to pass-through
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
def setup_application_and_window():
    """
    set up the application, application icon, and main window.
    args: parsed command-line arguments.
    returns: initialized application and window.
    """
    # fix high DPI issues
    fix_dpi()

    # initialize the PyQt application
    application = QApplication(sys.argv)
    application.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    # set the window icon and application name
    application.setWindowIcon(QIcon("./app/ui/resources/app_icon.ico"))
    application.setApplicationName("STARLAB COSMOS")
    
    window = MainWindow()
    
    return application, window


if __name__ == "__main__":

    # set up the application and main window
    application, window = setup_application_and_window()

    # start the application's event loop
    sys.exit(application.exec())
