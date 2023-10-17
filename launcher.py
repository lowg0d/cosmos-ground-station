"""
Used To Launch the Application
"""

import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from src import MainWindow


def main():
    """
    Initializes and starts the application.
    """
    # Fix high DPI issues
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Initialize the PyQt application
    application = QApplication(sys.argv)
    application.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # Set the window icon and application name
    icon_path = os.path.join(os.getcwd(), "app", "ui", "resources", "app_icon.ico")
    application.setWindowIcon(QIcon(icon_path))
    application.setApplicationName("STARLAB COSMOS")

    # Initialize the Window
    window = MainWindow(application)

    # Start the application's event loop
    sys.exit(application.exec())


if __name__ == "__main__":
    main()
