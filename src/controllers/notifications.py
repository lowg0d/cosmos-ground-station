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
from src.ui import Notification


class NotificationsController:
    DURATIONS = {
        "short": 1400,
        "medium": 2500,
        "long": 4500,
        "extraLong": 10000,
        "permanent": 1000000,
    }

    LEVELS = {
        "info": "badc58",
        "warning": "ffbe76",
        "error": "ff7979",
        "debug": "686de0",
    }

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.current_index = 0
        self.queue = []

    def new_msg(self, msg):
        bg = self.LEVELS["info"]
        duration = self.DURATIONS["short"]

        msg = msg.replace("\n", "")

        if len(msg) > 28:
            msg = self.insert_newlines(msg=msg)

        notification = Notification(
            parent=self.parent,
            message=msg,
            background=bg,
            duration=duration,
        )

        notification.closed.connect(self.nextInQueue)
        self.queue.append(notification)

        if len(self.queue) == 1:
            notification.display()

    def insert_newlines(self, msg, every=25):
        msg = msg.replace("\n", "")
        if len(msg) > every:
            msg = msg[:every] + "\n" + self.insert_newlines(msg[every:], every)
        return msg

    def new(self, level="info", duration="short", msg="Default Message"):
        bg = self.LEVELS[level]
        duration = self.DURATIONS[duration]
        msg = msg.replace("\n", " ")

        notification = Notification(
            parent=self.parent, message=msg, background=bg, duration=duration
        )

        notification.closed.connect(self.nextInQueue)
        self.queue.append(notification)

        if len(self.queue) == 1:
            notification.display()
            self.current_index = 0

    def nextInQueue(self):
        self.current_index += 1
        queueLen = len(self.queue)
        if queueLen >= self.current_index + 1:
            new = self.queue[(self.current_index)]
            new.display()

        else:
            self.queue = []
