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

from PyQt5.QtGui import QColor
from qframelesswindow import StandardTitleBar


# custom titlbear from PyQt Frameless Window (StandardTitleBar)
class CustomTitleBar(StandardTitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        # Customize the style of title bar buttons
        btns = [self.minBtn, self.maxBtn]
        for btn in btns:
            btn.setNormalColor(QColor(215, 215, 215))  # Set the normal button color
            btn.setHoverColor(QColor(215, 215, 215))  # Set the button color on hover
            btn.setPressedColor(
                QColor(215, 215, 215)
            )  # Set the button color when pressed
            btn.setHoverBackgroundColor(
                QColor(119, 110, 166)
            )  # Set the background color on hover
            btn.setPressedBackgroundColor(
                QColor(99, 90, 146)
            )  # Set the background color when pressed

        self.closeBtn.setNormalColor(QColor(215, 215, 215))  # Close button color
        self.closeBtn.setHoverColor(
            QColor(215, 215, 215)
        )  # Close button color on hover
        self.closeBtn.setPressedColor(
            QColor(215, 215, 215)
        )  # Close button color when pressed
        self.closeBtn.setHoverBackgroundColor(
            QColor(220, 69, 71)
        )  # Close button background color on hover
        self.closeBtn.setPressedBackgroundColor(
            QColor(150, 49, 51)
        )  # Close button background color when pressed
        # Change the font and center the title bar title
        self.titleLabel.setStyleSheet(
            """QLabel{
                margin: 0 0 0 5;
                background: transparent;
                font: 300 9.5pt "Video Light";
                color: rgba(245, 245, 245, 0.6);
                }"""  # Set the font color with transparency
        )
