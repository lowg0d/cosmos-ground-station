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

"""
This module contains the TerminalController class responsible for managing the terminal
functionality. The TerminalController handles writing messages, clearing the terminal,
and mantaining the line count under the maximum to ensure optimal performance.
"""

from PyQt5.QtCore import QTimer, QTime


class TerminalController:
    """
    This class manages the terminal functionality for the ground station application.
    It handles writing messages, clearing the terminal, and checking line count.
    """

    def __init__(self, parent):
        """
        Initializes the TerminalController.
        """
        self.parent = parent

        self.max_lines = 500
        self.terminal_clearer = QTimer()
        self.terminal_clearer.timeout.connect(self.check_line_count)
        self.terminal_clearer.start(30000)

    def write(self, data, custom_prefix=None):
        time_stamp = QTime.currentTime().toString("hh:mm:ss.zzz")
        if custom_prefix:
            message_prefix = f"[{time_stamp} <strong style='color:#786fa6';>{custom_prefix}</strong>]:"
        else:
            message_prefix = f"[{time_stamp}]:"

        message = f"\t<td>{message_prefix} <ins style='color:#a0a1a3'>{data}</td>"
        self.parent.ui.textBrowser_terminal.append(message)

    def clear(self):
        self.parent.ui.textBrowser_terminal.clear()

    def check_line_count(self):
        """
        Checks the line amount in the terminal and clears it if the threshold is exceeded.
        """
        if self.parent.ui.textBrowser_terminal.document().blockCount() > self.max_lines:
            self.clear()
