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
from PyQt5.QtGui import QColor

PEN_WIDTH = 2
ANTIALIAS = False
DATA_POINTS = 200
GPS_DATA_POINTS = 20
X_VALS = np.linspace(0.0, (DATA_POINTS - 1) / DATA_POINTS, DATA_POINTS)


class MonoAxePlotWidget(pg.PlotItem):
    def __init__(
        self,
        parent=None,
        title=None,
        labels={"bottom": "Time (s)"},
        name="plot_widget",
        color: str = "00BA42",
        enableMenu=False,
        **kwargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kwargs
        )

        color = f"#{color}" if color else "#e84118"
        # self.addLine(y=4000, pen='y')

        self.graph_plot = self.plot(
            x=X_VALS,
            y=np.zeros(DATA_POINTS),
            name=name,
            pen=pg.mkPen(color, width=PEN_WIDTH),
            antialias=ANTIALIAS,
            connect="finite",
            skipFiniteCheck=True,
        )
        self.graph_plot.pxMode = False
        self.graph_plot.setDownsampling(auto=True)

        self.curve = pg.PlotCurveItem()
        self.curve.pxMode = False
        self.addItem(self.curve)

        self.ptr1 = 0.0

        self.hideButtons()

        self.showGrid(x=True, y=True)

        self.getAxis("bottom").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setStyle(tickTextOffset=-35)

        self.getViewBox().disableAutoRange(axis="x")
        self.getViewBox().setMouseEnabled(x=False, y=False)

    def update(self, value):
        value = float(value)

        y_data = self.graph_plot.yData
        y_data[:-1] = y_data[1:]
        y_data[-1] = value

        self.ptr1 += 0.1
        x_vals = np.linspace(self.ptr1 - 0.1, self.ptr1, len(X_VALS))

        self.setXRange(self.ptr1 - 0.1, self.ptr1, padding=0.02)
        self.graph_plot.setData(x=x_vals, y=y_data)

    def clear(self):
        self.ptr1 = 0.0
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
        enableMenu=False,
        **kargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kargs
        )

        color_1 = f"#{color_1}" if color_1 else "#e84118"
        color_2 = f"#{color_2}" if color_2 else "#4cd137"

        self.addLegend()

        self.graph_plot_1 = self.plot(
            x=X_VALS,
            y=np.zeros(DATA_POINTS),
            name=name_1,
            pen=pg.mkPen(color_1, width=PEN_WIDTH),
            antialias=ANTIALIAS,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_2 = self.plot(
            x=X_VALS,
            y=np.zeros(DATA_POINTS),
            name=name_2,
            pen=pg.mkPen(color_2, width=PEN_WIDTH),
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

        self.ptr1 = 0.0

        self.hideButtons()

        self.showGrid(x=True, y=True)
        self.getAxis("bottom").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setStyle(tickTextOffset=-35)

        self.getViewBox().disableAutoRange(axis="x")
        self.getViewBox().setMouseEnabled(x=False, y=False)

    def update(self, value_1, value_2):
        value_1 = float(value_1)
        value_2 = float(value_2)

        y_data_1 = self.graph_plot_1.yData
        y_data_1[:-1] = y_data_1[1:]
        y_data_1[-1] = value_1

        y_data_2 = self.graph_plot_2.yData
        y_data_2[:-1] = y_data_2[1:]
        y_data_2[-1] = value_2

        self.ptr1 += 0.1
        x_vals = np.linspace(self.ptr1 - 0.1, self.ptr1, len(X_VALS))

        self.setXRange(self.ptr1 - 0.1, self.ptr1, padding=0.02)
        self.graph_plot_1.setData(x=x_vals, y=y_data_1)
        self.graph_plot_2.setData(x=x_vals, y=y_data_2)

    def clear(self):
        self.ptr1 = 0.0
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
        enableMenu=False,
        **kargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kargs
        )

        color_1 = f"#{color_1}" if color_1 else "#e84118"
        color_2 = f"#{color_2}" if color_2 else "#4cd137"
        color_3 = f"#{color_3}" if color_3 else "#00a8ff"

        self.addLegend()

        self.graph_plot_1 = self.plot(
            x=X_VALS,
            y=np.zeros(DATA_POINTS),
            name=name_1,
            pen=pg.mkPen(color_1, width=PEN_WIDTH),
            antialias=ANTIALIAS,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_2 = self.plot(
            x=X_VALS,
            y=np.zeros(DATA_POINTS),
            name=name_2,
            pen=pg.mkPen(color_2, width=PEN_WIDTH),
            antialias=ANTIALIAS,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_3 = self.plot(
            x=X_VALS,
            y=np.zeros(DATA_POINTS),
            name=name_3,
            pen=pg.mkPen(color_3, width=PEN_WIDTH),
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

        self.ptr1 = 0.0

        self.hideButtons()

        self.showGrid(x=True, y=True)
        self.getAxis("bottom").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setStyle(tickTextOffset=-35)

        self.getViewBox().disableAutoRange(axis="x")
        self.getViewBox().setMouseEnabled(x=False, y=False)

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

        self.ptr1 += 0.1
        x_vals = np.linspace(self.ptr1 - 0.1, self.ptr1, len(X_VALS))

        self.setXRange(self.ptr1 - 0.1, self.ptr1, padding=0.02)
        self.graph_plot_1.setData(x=x_vals, y=y_data_1)
        self.graph_plot_2.setData(x=x_vals, y=y_data_2)
        self.graph_plot_3.setData(x=x_vals, y=y_data_3)

    def clear(self):
        self.ptr1 = 0.0
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
            pen=pg.mkPen(smooth_color, width=2),
            antialias=False,
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

        self.hideButtons()
        self.getViewBox().setMouseEnabled(x=False, y=False)

    def update(self, value_1, value_2):
        value_1 = float(value_1)
        value_2 = float(value_2)

        self.graph_data["x"].append(value_1)
        self.graph_data["y"].append(value_2)

        if len(self.graph_data["x"]) > 70:
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
        self.setRange(xRange=x_range, yRange=y_range, padding=1.5)

    def clear(self):
        self.graph_data = {"x": [], "y": []}
        self.lastet_data = {"x": [], "y": []}
        self.ptr1 = 0.0
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
        self.ptr1 = 0.0
        self.update(0.0, 0.0)
