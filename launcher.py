"""
Used To Launch the Application
"""

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from src import MainWindow

if __name__ == "__main__":

    # Fix high DPI issues
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Initialize the PyQt application
    application = QApplication(sys.argv)
    application.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # Set the window icon and application name
    application.setWindowIcon(QIcon("./app/ui/resources/app_icon.ico"))
    application.setApplicationName("STARLAB COSMOS")

    # Initialize the Window
    window = MainWindow()

    # Start the application's event loop
    sys.exit(application.exec())
