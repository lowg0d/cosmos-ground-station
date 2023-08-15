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

"""
NOTE: 
TODO: 
- restart button.
- open the records folder.
- cloud, auth and file upload.
- turn toggle small button, into menu button, with a lot more of options
- separate the profiles

IDEAS:
- rocket and satellite mode ?
- multi sage mode with tabs.
- Graphical Replay Interface, and recovery tool. (reconstruct logs from arduino etc...)
- Socket interconnection.
- Missions:
    - pre flight checks. (with the phone ? web)
    - shared profile.
    - shared countdown.
    - with the same google account
- Graphical Editor For Profiles.
- Multi Lenguage
- refactor for data donde by ai
"""

import os
import sys
import logging
import argparse

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from src import Window


def parse_arguments():
    """
    parse command-line arguments
    returns: parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-debug", action="store_true", help="Enable debugging mode")
    return parser.parse_args()


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


def setup_logger(debug):
    """
    set up logging with custom formatting and log levels.
    args: enable debugging mode if True.
    returns: configured logger instance.
    """
    # define the log message format and different log level formats
    FMT = "{asctime} {name}: \33[1m{message}"
    FORMATS = {
        logging.DEBUG: f"\33[1m\33[34m(D)\33[0m \33[34m{FMT}\33[0m",
        logging.INFO: f"\33[1m\33[32m(I)\33[0m \33[32m{FMT}\33[0m",
        logging.WARNING: f"\33[1m\33[33m(W)\33[0m \33[1m\33[33m{FMT}\33[0m",
        logging.ERROR: f"\33[1m\33[31;m(E)\33[0m \33[1m\33[31m{FMT}\33[0m",
        logging.CRITICAL: f"\33[1m\33[31;1m(C)\33[0m \33[1m\33[31;1m{FMT}\33[0m",
    }

    # custom formatter for logging
    class CustomFormatter(logging.Formatter):
        def format(self, record):
            log_fmt = FORMATS.get(record.levelno, f"{FMT}")
            formatter = logging.Formatter(log_fmt, style="{")
            return formatter.format(record)

    # create a logging handler and set the custom formatter
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())

    # determine the log level based on the 'debug' attribute and configure the root logger
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=level, handlers=[handler])

    # get a named logger instance and return it
    logger = logging.getLogger("cosmos")
    logger.debug("initializing cosmos in DEBUG mode")

    return logger


def setup_application(parsed_args):
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
    application.setWindowIcon(QIcon("./app/ui/assets/app_icon.ico"))
    application.setApplicationName("STARLAB COSMOS")

    # get the logger
    logger = setup_logger(parsed_args.debug)

    # initialize the main application window
    window = Window(debug=parsed_args.debug, logger=logger)
    return application, window


if __name__ == "__main__":
    # parse command-line arguments
    parsed_args = parse_arguments()

    # set up the application and main window
    application, window = setup_application(parsed_args)

    # start the application's event loop
    sys.exit(application.exec())
