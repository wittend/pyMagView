#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
nbPlotClass.py

plotting classes

author: David Witten
last modified: December 2020
"""
import wx
import numpy as np
from wx.lib import plot as wxplot
from wx.lib.plot import PlotCanvas 
from wx.lib.plot import PlotGraphics
from wx.lib.plot import  PolyLine
from wx.lib.plot import  PolyMarker

# class nbPlotSimple(wx.Panel):
#     """
#         class nbPlotSimple()
#     """
#     def __init__(self, parent, data):
#         """
#             __init__()
#         """
#         super(nbPlotSimple, self).__init__()
#         self.InitUI(parent)
#         
#         
#     def InitUI(self, parent):
#         self.plotCtrl = wx.Panel.__init__(
#                 self,
#                 parent,
#                 -1
#                 # style= wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES
#             )
def createPlot(self, parent):
    #self.attr1.SetBackgroundColour("#d5ffb0")
    t = np.arange(0.0, 3.0, 0.01)
    s = np.sin(2.5 * np.pi * t)
    #markers1 = PolyMarker(data1, legend='Green Markers', colour='green', marker='circle',size=1)
    x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    y_data = [2, 4, 6, 4, 2, 5, 6, 7, 1]
    self.nbplot = PlotCanvas(self.topRightNBookPlot, wx.ID_ANY)
    #self.nbplot = PlotCanvas(parent, wx.ID_ANY)
    self.nbplot.enableXAxisLabel = True
    self.nbplot.enableYAxisLabel = True
    self.nbplot.enableTitle = True
    self.nbplot.enableGrid = True
    self.nbplot.enableAntiAliasing = True
    #self.nbplot.enableAxesValues({bottom, left})
    #self.nbplot.enableTicks({bottom, left})

    #self.nbplot(t, s)
    self.nbplot.xlabel = 'time (s)'
    self.nbplot.ylabel = 'voltage (mV)'

    self.nbplot.title = 'Sine Wave'
    #self.nbplot.grid(True)

    xy_data = list(zip(x_data, y_data))
    # Use keyword args to set display properties.
    line = wxplot.PolySpline(
        xy_data,
        colour=wx.Colour(128, 128, 0),   # Color: olive
        width=3,
    )
    # create your graphics object
    graphics = wxplot.PlotGraphics([line])
    # Edit panel-wide settings
    axes_pen = wx.Pen(wx.BLUE, 1, wx.PENSTYLE_LONG_DASH)
    self.nbplot.axesPen = axes_pen
    # draw the graphics object on the canvas
    self.nbplot.Draw(graphics)
    #sizerNBPlot.Add(self.nbplot, 1, wx.EXPAND, 0)
