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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QAbstractAnimation, pyqtSignal


class Notification(QtWidgets.QFrame):
    closed = pyqtSignal()

    def __init__(self, parent, message, background, duration):
        super().__init__(parent)
        QtWidgets.QHBoxLayout(self)

        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        self.setStyleSheet(
            f"""
                border-radius: 4px; 
                padding-left: 4px;
                padding-right: 2px;
                padding-top: 2px;
                padding-bottom: 2px;
                color: #98999b;
                background-color: #{background};
            """
        )

        self.timer = QtCore.QTimer(singleShot=True, timeout=self.hide)

        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(opacity=0)
        self.setGraphicsEffect(self.opacityEffect)

        self.opacityAni = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity")
        self.closedOpacityAni = QtCore.QPropertyAnimation(
            self.opacityEffect, b"opacity"
        )
        self.parent().installEventFilter(self)

        self.opacityAni.setStartValue(0.0)
        self.opacityAni.setEndValue(0.8)
        self.opacityAni.setDuration(100)

        self.closedOpacityAni.setStartValue(0.8)
        self.closedOpacityAni.setEndValue(0.0)
        self.closedOpacityAni.setDuration(200)
        self.closedOpacityAni.finished.connect(self.close)

        self.incoming = None

        self.corner = QtCore.Qt.BottomRightCorner
        self.margin = 10

        parent = parent.window()
        parentRect = parent.rect()

        self.timer.setInterval(duration)

        self.message = message
        self.label = QtWidgets.QLabel(f"{message}")

        self.label.setStyleSheet(f"color: #303236; background-color: #{background};")

        font = QtGui.QFont("Video Med", 10)
        self.label.setFont(font)
        self.layout().addWidget(self.label)

        self.closeButton = QtWidgets.QToolButton()
        self.layout().addWidget(self.closeButton)
        closeIcon = self.style().standardIcon(QtWidgets.QStyle.SP_TitleBarCloseButton)
        self.closeButton.setIcon(closeIcon)
        self.closeButton.setAutoRaise(True)
        self.closeButton.setStyleSheet("background: transparent")
        self.closeButton.clicked.connect(self.close)

        # raise the widget and adjust its size to the minimum
        self.raise_()
        self.adjustSize()

        margin = self.margin

        geo = self.geometry()
        geo.moveBottomRight(parentRect.bottomRight() + QtCore.QPoint(-margin, -margin))

        self.setGeometry(geo)

        self.counter = 0

    def display(self):
        self.show()
        self.timer.start()
        self.opacityAni.start()

    def hide(self):
        self.closedOpacityAni.start()

    def restore(self):
        self.timer.stop()
        self.closedOpacityAni.stop()
        if self.parent():
            self.opacityEffect.setOpacity(0.8)
        else:
            self.setWindowOpacity(0.8)

    def enterEvent(self, e):
        self.restore()

    def leaveEvent(self, e):
        self.timer.start()

    def closeEvent(self, e):
        self.deleteLater()
        self.closed.emit()

    def eventFilter(self, source, e):
        if source == self.parent() and e.type() == QtCore.QEvent.Resize:
            self.opacityAni.stop()
            parentRect = self.parent().rect()
            geo = self.geometry()
            geo.moveBottomRight(
                parentRect.bottomRight() + QtCore.QPoint(-self.margin, -self.margin)
            )
            self.setGeometry(geo)
            self.restore()
            self.timer.start()

        return super(Notification, self).eventFilter(source, e)

    def resizeEvent(self, e):
        super(Notification, self).resizeEvent(e)
        # if you don't set a stylesheet, you don't need any of the following!
        if not self.parent():
            # there's no parent, so we need to update the mask
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(self.rect()).translated(-0.8, -0.8), 4, 4)
            self.setMask(
                QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
            )
        else:
            self.clearMask()
