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

import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import QColor

pen_width = 2.2
LINSPACE = 11

class MonoAxePlotWidget(pg.PlotItem):
    def __init__(
        self,
        parent=None,
        title=None,
        labels={"bottom": "Time (s)"},
        name="plot_widget",
        color: str = "00BA42",
        enableMenu=False,
        linspace_x=LINSPACE,
        **kargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kargs
        )

        if color == None:
            color = "e84118"

        color = f"#{color}"

        x_vals = np.linspace(0.0, (linspace_x - 1) / linspace_x, linspace_x)
        self.graph_plot = self.plot(
            x=x_vals,
            name=name,
            pen=pg.mkPen(color, width=pen_width),
            antialias=True,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot.pxMode = False

        self.graph_plot.setDownsampling(auto=True)
        self.graph_data = np.zeros(linspace_x)

        self.curve = pg.PlotCurveItem()
        self.curve.pxMode = False
        self.addItem(self.curve)

        self.ptr1 = 0.0
        self.window_size = 10
        self.weights = np.ones(self.window_size) / self.window_size

        self.showGrid(x=True, y=True)

        # Set custom label style
        self.getAxis("bottom").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setStyle(tickTextOffset=-40)

        self.getViewBox().disableAutoRange(axis="x")
        self.getViewBox().setMouseEnabled(x=False, y=False)
        self.hideButtons()

    def update(self, value):
        value = float(value)

        self.graph_data[:-1] = self.graph_data[1:]
        self.graph_data[-1] = value

        x_vals = np.linspace(self.ptr1, self.ptr1 + 0.1, len(self.graph_data))
        self.ptr1 += 0.1

        self.graph_plot.setData(x=x_vals, y=self.graph_data)
        self.setXRange(self.ptr1 - 0.1, self.ptr1, padding=0.01)

    def clear(self):
        self.ptr1 = 0.0
        self.graph_data = np.zeros_like(self.graph_data)
        self.graph_plot.clear()
        self.curve.clear()
        self.update(0.0)

class DualAxePlotWidget(pg.PlotItem):
    def __init__(
        self,
        parent=None,
        labels={"bottom": "T(s)"},
        title=None,
        color_x: str = "00d2d3",
        color_y: str = "ff9ff3",
        name_x="X",
        name_y="Y",
        enableMenu=False,
        linspace_x=LINSPACE,
        **kargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kargs
        )

        self.name_x = name_x
        self.name_y = name_y

        if color_x == None:
            color_x = "e84118"
        if color_y == None:
            color_y = "4cd137"

        color_x = f"#{color_x}"
        color_y = f"#{color_y}"

        x_vals_x = np.linspace(0.0, (linspace_x - 1) / linspace_x, linspace_x)
        x_vals_y = np.linspace(0.0, (linspace_x - 1) / linspace_x, linspace_x)

        fill_color_x = QColor(color_x)
        fill_color_x.setAlpha(20)

        fill_color_y = QColor(color_y)
        fill_color_y.setAlpha(20)

        self.addLegend()

        self.graph_plot_x = self.plot(
            x=x_vals_x,
            name=name_x,
            pen=pg.mkPen(color_x, width=pen_width),
            antialias=True,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_y = self.plot(
            x=x_vals_y,
            name=name_y,
            pen=pg.mkPen(color_y, width=pen_width),
            antialias=True,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_x.pxMode = False
        self.graph_plot_y.pxMode = False

        self.graph_plot_x.setDownsampling(auto=True)
        self.graph_plot_y.setDownsampling(auto=True)

        self.graph_data_x = np.zeros(linspace_x)
        self.graph_data_y = np.zeros(linspace_x)

        self.curve = pg.PlotCurveItem()
        self.curve.pxMode = False
        self.addItem(self.curve)

        self.ptr1 = 0.0
        self.window_size = 5
        self.weights = np.ones(self.window_size) / self.window_size

        self.showGrid(x=True, y=True)
        self.getAxis("bottom").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setStyle(tickTextOffset=-40)

        self.getViewBox().disableAutoRange(axis="x")
        self.hideButtons()
        self.getViewBox().setMouseEnabled(x=False, y=False)

    def update(self, value_x, value_y):
        value_x = float(value_x)
        value_y = float(value_y)

        self.graph_data_x[:-1] = self.graph_data_x[1:]
        self.graph_data_x[-1] = value_x

        self.graph_data_y[:-1] = self.graph_data_y[1:]
        self.graph_data_y[-1] = value_y

        x_vals_x = np.linspace(self.ptr1, self.ptr1 + 0.1, len(self.graph_data_x))
        x_vals_y = np.linspace(self.ptr1, self.ptr1 + 0.1, len(self.graph_data_y))

        self.ptr1 += 0.1

        self.setXRange(self.ptr1 - 0.1, self.ptr1, padding=0.01)
        self.graph_plot_x.setData(x=x_vals_x, y=self.graph_data_x)
        self.graph_plot_y.setData(x=x_vals_y, y=self.graph_data_y)

    def clear(self):
        self.ptr1 = 0.0
        self.graph_data_x = np.zeros_like(self.graph_data_x)
        self.graph_data_y = np.zeros_like(self.graph_data_y)

        self.graph_plot_x.clear()
        self.graph_plot_y.clear()

        self.curve.clear()

        self.update(0.0, 0.0)

class TripleAxePlotWidget(pg.PlotItem):
    def __init__(
        self,
        parent=None,
        labels={"bottom": "T(s)"},
        title=None,
        color_x: str = "e84118",
        color_y: str = "4cd137",
        color_z: str = "00a8ff",
        name_x="X",
        name_y="Y",
        name_z="Z",
        enableMenu=False,
        linspace_x=LINSPACE,
        **kargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kargs
        )

        self.name_x = name_x
        self.name_y = name_y
        self.name_z = name_z

        if color_x == None:
            color_x = "e84118"
        if color_y == None:
            color_y = "4cd137"
        if color_z == None:
            color_z = "00a8ff"

        color_x = f"#{color_x}"
        color_y = f"#{color_y}"
        color_z = f"#{color_z}"

        x_vals_x = np.linspace(0.0, (linspace_x - 1) / linspace_x, linspace_x)
        x_vals_y = np.linspace(0.0, (linspace_x - 1) / linspace_x, linspace_x)
        x_vals_z = np.linspace(0.0, (linspace_x - 1) / linspace_x, linspace_x)

        self.addLegend()

        self.graph_plot_x = self.plot(
            x=x_vals_x,
            name=name_x,
            pen=pg.mkPen(color_x, width=pen_width),
            antialias=True,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_y = self.plot(
            x=x_vals_y,
            name=name_y,
            pen=pg.mkPen(color_y, width=pen_width),
            antialias=True,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_z = self.plot(
            x=x_vals_z,
            name=name_z,
            pen=pg.mkPen(color_z, width=2),
            antialias=True,
            connect="finite",
            skipFiniteCheck=True,
        )

        self.graph_plot_x.pxMode = False
        self.graph_plot_y.pxMode = False
        self.graph_plot_z.pxMode = False

        self.graph_plot_x.setDownsampling(auto=True)
        self.graph_plot_y.setDownsampling(auto=True)
        self.graph_plot_z.setDownsampling(auto=True)

        self.graph_data_x = np.zeros(linspace_x)
        self.graph_data_y = np.zeros(linspace_x)
        self.graph_data_z = np.zeros(linspace_x)

        self.curve = pg.PlotCurveItem()
        self.curve.pxMode = False
        self.addItem(self.curve)

        self.ptr1 = 0.0
        self.window_size = 5
        self.weights = np.ones(self.window_size) / self.window_size

        self.showGrid(x=True, y=True)
        self.getAxis("bottom").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setPen(pg.mkPen("#a5a5a5"))
        self.getAxis("left").setStyle(tickTextOffset=-40)

        self.getViewBox().disableAutoRange(axis="x")
        self.hideButtons()
        self.getViewBox().setMouseEnabled(x=False, y=False)

    def update(self, value_x, value_y, value_z):
        value_x = float(value_x)
        value_y = float(value_y)
        value_z = float(value_z)

        self.graph_data_x[:-1] = self.graph_data_x[1:]
        self.graph_data_x[-1] = value_x

        self.graph_data_y[:-1] = self.graph_data_y[1:]
        self.graph_data_y[-1] = value_y

        self.graph_data_z[:-1] = self.graph_data_z[1:]
        self.graph_data_z[-1] = value_z

        x_vals_x = np.linspace(self.ptr1, self.ptr1 + 0.1, len(self.graph_data_x))
        x_vals_y = np.linspace(self.ptr1, self.ptr1 + 0.1, len(self.graph_data_y))
        x_vals_z = np.linspace(self.ptr1, self.ptr1 + 0.1, len(self.graph_data_z))

        self.ptr1 += 0.1

        self.setXRange(self.ptr1 - 0.1, self.ptr1, padding=0.01)
        self.graph_plot_x.setData(x=x_vals_x, y=self.graph_data_x)
        self.graph_plot_y.setData(x=x_vals_y, y=self.graph_data_y)
        self.graph_plot_z.setData(x=x_vals_z, y=self.graph_data_z)

    def clear(self):
        self.ptr1 = 0.0
        self.graph_data_x = np.zeros_like(self.graph_data_x)
        self.graph_data_y = np.zeros_like(self.graph_data_y)
        self.graph_data_z = np.zeros_like(self.graph_data_z)

        self.graph_plot_x.clear()
        self.graph_plot_y.clear()
        self.graph_plot_z.clear()

        self.curve.clear()

        self.update(0.0, 0.0, 0.0)

# ================================================================= #
class GpsPlotWidget(pg.PlotItem):
    def __init__(
        self,
        parent=None,
        labels={"bottom": "Longitude", "left": "Latitude"},
        title=None,
        color: str = "00BA42",
        enableMenu=False,
        **kargs,
    ):
        super().__init__(
            parent=parent, labels=labels, title=title, enableMenu=enableMenu, **kargs
        )

        if color == None:
            color = "e84118"

        color = f"#{color}"

        fill_color = QColor(color)
        fill_color.setAlpha(80)

        self.graph_data = {"x": [], "y": []}
        self.lastet_data = {"x": [], "y": []}

        self.graph_plot = self.plot(
            pen=pg.mkPen(fill_color, width=2),
            antialias=True,
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
            min(self.graph_data["x"]) - 0.0190,
            max(self.graph_data["x"]) + 0.0190,
        )
        y_range = (
            min(self.graph_data["y"]) - 0.0190,
            max(self.graph_data["y"]) + 0.0190,
        )
        self.setRange(xRange=x_range, yRange=y_range, padding=0.03)
