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
import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import QColor, QFont

PEN_WIDTH = 1.5
ANTIALIAS = True
DATA_POINTS = 250
GPS_DATA_POINTS = 100
X_VALS = np.linspace(0.0, (DATA_POINTS - 1) / DATA_POINTS, DATA_POINTS)
FONT = QFont("Video Med", 9)


class MonoAxePlotWidget(pg.PlotItem):
    def __init__(
        self,
        parent=None,
        title=None,
        labels={"bottom": "Time (s)"},
        name="plot_widget",
        color: str = "00BA42",
        enableMenu=True,
        pen_width=PEN_WIDTH,
        datapoints=DATA_POINTS,
        unit="",
        **kwargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kwargs
        )

        color = f"#{color}" if color else "#e84118"
        datapoints = datapoints if datapoints else DATA_POINTS
        pen_width = pen_width if pen_width else PEN_WIDTH
        # self.addLine(y=4000, pen='y')

        self.x_vals = np.linspace(0.0, (datapoints - 1) / datapoints, datapoints)
        self.graph_plot = self.plot(
            x=self.x_vals,
            y=np.zeros(datapoints),
            name=name,
            pen=pg.mkPen(color, width=pen_width),
            antialias=ANTIALIAS,
            connect="finite",
            skipFiniteCheck=True,
        )
        self.graph_plot.pxMode = False
        self.graph_plot.setDownsampling(auto=True)

        self.curve = pg.PlotCurveItem()

        self.curve.pxMode = False
        self.addItem(self.curve)

        self.y_vals = 0.0

        self.hideButtons()
        self.showGrid(x=True, y=True)

        self.getAxis("bottom").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setStyle(tickTextOffset=-35)

        # TEMPORAL (
        self.getAxis("bottom").label.setFont(FONT)
        self.getAxis("left").label.setFont(FONT)
        self.titleLabel.item.setFont(FONT)
        # )

        self.getViewBox().disableAutoRange(axis="x")
        self.getViewBox().setMouseEnabled(x=False, y=False)

        self.dataPointsIndex = 1

    def update(self, value):
        value = float(value)

        y_data = self.graph_plot.yData
        y_data[:-1] = y_data[1:]
        y_data[-1] = value

        self.y_vals += 0.1
        x_vals = np.linspace(self.y_vals - 0.1, self.y_vals, len(self.x_vals))

        self.setXRange(self.y_vals - 0.1, self.y_vals, padding=0.02)
        self.graph_plot.setData(x=x_vals, y=y_data)

    def change_color(self, color):
        self.getAxis("bottom").setPen(pg.mkPen(color))
        self.getAxis("left").setPen(pg.mkPen(color))

    def clear(self):
        self.y_vals = 0.0
        self.graph_plot.yData[:] = 0.0
        self.curve.clear()
        self.update(0.0)


class DualAxePlotWidget(pg.PlotItem):
    def __init__(
        self,
        parent=None,
        labels={"bottom": "T(s)"},
        title=None,
        color_1: str = "00d2d3",
        color_2: str = "ff9ff3",
        name_1="X",
        name_2="Y",
        enableMenu=True,
        pen_width=PEN_WIDTH,
        datapoints=DATA_POINTS,
        **kargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kargs
        )

        self.addLegend()

        color_1 = f"#{color_1}" if color_1 else "#e84118"
        color_2 = f"#{color_2}" if color_2 else "#4cd137"

        name_1 = "X" if not name_1 else name_1
        name_2 = "X" if not name_2 else name_2

        datapoints = datapoints if datapoints else DATA_POINTS
        pen_width = pen_width if pen_width else PEN_WIDTH

        self.x_vals = np.linspace(0.0, (datapoints - 1) / datapoints, datapoints)
        self.graph_plot_1 = self.plot(
            x=self.x_vals,
            y=np.zeros(datapoints),
            name=name_1,
            pen=pg.mkPen(color_1, width=pen_width),
            antialias=ANTIALIAS,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_2 = self.plot(
            x=self.x_vals,
            y=np.zeros(datapoints),
            name=name_2,
            pen=pg.mkPen(color_2, width=pen_width),
            antialias=ANTIALIAS,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_1.pxMode = False
        self.graph_plot_2.pxMode = False

        self.graph_plot_1.setDownsampling(auto=True)
        self.graph_plot_2.setDownsampling(auto=True)

        self.curve = pg.PlotCurveItem()
        self.curve.pxMode = False
        self.addItem(self.curve)

        self.y_vals = 0.0

        self.hideButtons()

        self.showGrid(x=True, y=True)
        self.getAxis("bottom").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setStyle(tickTextOffset=-35)

        # TEMPORAL (
        self.getAxis("bottom").label.setFont(FONT)
        self.getAxis("left").label.setFont(FONT)
        self.titleLabel.item.setFont(FONT)
        # )

        self.getViewBox().disableAutoRange(axis="x")
        self.getViewBox().setMouseEnabled(x=False, y=False)

    def change_color(self, color):
        self.getAxis("bottom").setPen(pg.mkPen(color))
        self.getAxis("left").setPen(pg.mkPen(color))

    def update(self, value_1, value_2):
        value_1 = float(value_1)
        value_2 = float(value_2)

        y_data_1 = self.graph_plot_1.yData
        y_data_1[:-1] = y_data_1[1:]
        y_data_1[-1] = value_1

        y_data_2 = self.graph_plot_2.yData
        y_data_2[:-1] = y_data_2[1:]
        y_data_2[-1] = value_2

        self.y_vals += 0.1
        x_vals = np.linspace(self.y_vals - 0.1, self.y_vals, len(self.x_vals))

        self.setXRange(self.y_vals - 0.1, self.y_vals, padding=0.02)
        self.graph_plot_1.setData(x=x_vals, y=y_data_1)
        self.graph_plot_2.setData(x=x_vals, y=y_data_2)

    def clear(self):
        self.y_vals = 0.0
        self.graph_plot_1.yData[:] = 0.0
        self.graph_plot_2.yData[:] = 0.0
        self.curve.clear()
        self.update(0.0, 0.0)


class TripleAxePlotWidget(pg.PlotItem):
    def __init__(
        self,
        parent=None,
        labels={"bottom": "T(s)"},
        title=None,
        color_1: str = "e84118",
        color_2: str = "4cd137",
        color_3: str = "00a8ff",
        name_1="X",
        name_2="Y",
        name_3="Z",
        enableMenu=True,
        pen_width=PEN_WIDTH,
        datapoints=DATA_POINTS,
        **kargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kargs
        )

        self.addLegend()

        color_1 = f"#{color_1}" if color_1 else "#e84118"
        color_2 = f"#{color_2}" if color_2 else "#4cd137"
        color_3 = f"#{color_3}" if color_3 else "#00a8ff"

        datapoints = datapoints if datapoints else DATA_POINTS
        pen_width = pen_width if pen_width else PEN_WIDTH

        self.x_vals = np.linspace(0.0, (datapoints - 1) / datapoints, datapoints)
        self.graph_plot_1 = self.plot(
            x=self.x_vals,
            y=np.zeros(datapoints),
            name=name_1,
            pen=pg.mkPen(color_1, width=pen_width),
            antialias=ANTIALIAS,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_2 = self.plot(
            x=self.x_vals,
            y=np.zeros(datapoints),
            name=name_2,
            pen=pg.mkPen(color_2, width=pen_width),
            antialias=ANTIALIAS,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_3 = self.plot(
            x=self.x_vals,
            y=np.zeros(datapoints),
            name=name_3,
            pen=pg.mkPen(color_3, width=pen_width),
            antialias=ANTIALIAS,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_1.pxMode = False
        self.graph_plot_2.pxMode = False
        self.graph_plot_3.pxMode = False

        self.graph_plot_1.setDownsampling(auto=True)
        self.graph_plot_2.setDownsampling(auto=True)
        self.graph_plot_3.setDownsampling(auto=True)

        self.curve = pg.PlotCurveItem()
        self.curve.pxMode = False
        self.addItem(self.curve)

        self.y_vals = 0.0

        self.hideButtons()

        self.showGrid(x=True, y=True)
        self.getAxis("bottom").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setStyle(tickTextOffset=-35)

        # TEMPORAL (
        self.getAxis("bottom").label.setFont(FONT)
        self.getAxis("left").label.setFont(FONT)
        self.titleLabel.item.setFont(FONT)
        # )

        self.getViewBox().disableAutoRange(axis="x")
        self.getViewBox().setMouseEnabled(x=False, y=False)

    def change_color(self, color):
        self.getAxis("bottom").setPen(pg.mkPen(color))
        self.getAxis("left").setPen(pg.mkPen(color))

    def update(self, value_1, value_2, value_3):
        value_1 = float(value_1)
        value_2 = float(value_2)
        value_3 = float(value_3)

        y_data_1 = self.graph_plot_1.yData
        y_data_1[:-1] = y_data_1[1:]
        y_data_1[-1] = value_1

        y_data_2 = self.graph_plot_2.yData
        y_data_2[:-1] = y_data_2[1:]
        y_data_2[-1] = value_2

        y_data_3 = self.graph_plot_3.yData
        y_data_3[:-1] = y_data_3[1:]
        y_data_3[-1] = value_3

        self.y_vals += 0.1
        x_vals = np.linspace(self.y_vals - 0.1, self.y_vals, len(self.x_vals))

        self.setXRange(self.y_vals - 0.1, self.y_vals, padding=0.02)
        self.graph_plot_1.setData(x=x_vals, y=y_data_1)
        self.graph_plot_2.setData(x=x_vals, y=y_data_2)
        self.graph_plot_3.setData(x=x_vals, y=y_data_3)

    def clear(self):
        self.y_vals = 0.0
        self.graph_plot_1.yData[:] = 0.0
        self.graph_plot_2.yData[:] = 0.0
        self.graph_plot_3.yData[:] = 0.0
        self.curve.clear()
        self.update(0.0, 0.0, 0.0)


class GpsPlotWidget(pg.PlotItem):
    def __init__(
        self,
        parent=None,
        labels={"bottom": "Longitude", "left": "Latitude"},
        title=None,
        color: str = "ffc048",
        enableMenu=True,
        pen_width=PEN_WIDTH,
        datapoints=GPS_DATA_POINTS,
        **kargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kargs
        )

        color = f"#{color}" if color else "#ffc048"
        datapoints = datapoints if datapoints else GPS_DATA_POINTS
        pen_width = pen_width if pen_width else PEN_WIDTH

        self.datapoints = datapoints
        smooth_color = QColor(color)
        # smooth_color.setAlpha(90)

        self.graph_data = {"x": [], "y": []}
        self.lastet_data = {"x": [], "y": []}

        self.graph_plot = self.plot(
            pen=pg.mkPen(smooth_color, width=pen_width),
            antialias=ANTIALIAS,
            connect="finite",
            symbol=None,
        )

        self.graph_plot.setDownsampling(auto=True)
        self.graph_plot.pxMode = False

        self.scatter_plot = pg.ScatterPlotItem(
            symbol="o", size=6, brush=pg.mkBrush(color)
        )
        self.addItem(self.scatter_plot)

        self.showGrid(x=True, y=True)
        self.getAxis("bottom").setPen(pg.mkPen("#777"))
        self.getAxis("left").setPen(pg.mkPen("#777"))

        # TEMPORAL (
        self.getAxis("bottom").label.setFont(FONT)
        self.getAxis("left").label.setFont(FONT)
        self.titleLabel.item.setFont(FONT)
        # )

        self.hideButtons()
        self.getViewBox().setMouseEnabled(x=False, y=False)

    def change_color(self, color):
        self.getAxis("bottom").setPen(pg.mkPen(color))
        self.getAxis("left").setPen(pg.mkPen(color))

    def update(self, value_1, value_2):
        value_1 = float(value_1)
        value_2 = float(value_2)

        self.graph_data["x"].append(value_1)
        self.graph_data["y"].append(value_2)

        if len(self.graph_data["x"]) > self.datapoints:
            self.graph_data["x"].pop(0)
            self.graph_data["y"].pop(0)

        self.lastet_data = {"x": [value_1], "y": [value_2]}
        self.graph_plot.setData(self.graph_data["x"], self.graph_data["y"])
        self.scatter_plot.setData(
            self.lastet_data["x"], self.lastet_data["y"], symbol="o", connect="finite"
        )

        x_range = (
            min(self.graph_data["x"]) - 0.0001,
            max(self.graph_data["x"]) + 0.0001,
        )
        y_range = (
            min(self.graph_data["y"]) - 0.0001,
            max(self.graph_data["y"]) + 0.0001,
        )
        self.setRange(xRange=x_range, yRange=y_range, padding=2.5)

    def clear(self):
        self.graph_data = {"x": [], "y": []}
        self.lastet_data = {"x": [], "y": []}
        self.y_vals = 0.0
        self.update(0.0, 0.0)


class GpsPlotWidget1(pg.PlotItem):
    def __init__(
        self,
        parent=None,
        labels={"bottom": "Longitude", "left": "Latitude"},
        title=None,
        color: str = "ffc048",
        enableMenu=False,
        **kargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kargs
        )

        color = f"#{color}" if color else "#ffc048"

        smooth_color = QColor(color)
        smooth_color.setAlpha(90)

        self.graph_data = {"x": [], "y": []}
        self.lastet_data = {"x": [], "y": []}

        self.graph_plot = self.plot(
            pen=pg.mkPen(smooth_color, width=PEN_WIDTH),
            antialias=False,
            connect="finite",
            symbol=None,
        )

        self.graph_plot.setDownsampling(auto=True)
        self.graph_plot.pxMode = False

        self.scatter_plot = pg.ScatterPlotItem(
            symbol="x", size=7, brush=pg.mkBrush(color)
        )
        self.addItem(self.scatter_plot)

        self.showGrid(x=True, y=True)
        self.getAxis("bottom").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setPen(pg.mkPen("#a5a5a5"))

        self.hideButtons()
        self.getViewBox().setMouseEnabled(x=False, y=False)

    def update(self, latitude, longitude):
        longitude = float(longitude)
        latitude = float(latitude)

        self.graph_data["x"].append(longitude)
        self.graph_data["y"].append(latitude)

        if len(self.graph_data["x"]) > 40:
            self.graph_data["x"].pop(0)
            self.graph_data["y"].pop(0)

        self.lastet_data = {"x": [longitude], "y": [latitude]}
        self.graph_plot.setData(self.graph_data["x"], self.graph_data["y"])
        self.scatter_plot.setData(
            self.lastet_data["x"],
            self.lastet_data["y"],
            symbol="o",
            connect="finite",
            size=8,
        )

        x_range = (
            min(self.graph_data["x"]) - 0.0090,
            max(self.graph_data["x"]) + 0.0090,
        )
        y_range = (
            min(self.graph_data["y"]) - 0.0090,
            max(self.graph_data["y"]) + 0.0090,
        )
        self.setRange(xRange=x_range, yRange=y_range, padding=1.53)

    def clear(self):
        self.graph_data = {"x": [], "y": []}
        self.lastet_data = {"x": [], "y": []}
        self.y_vals = 0.0
        self.update(0.0, 0.0)
