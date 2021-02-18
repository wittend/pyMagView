#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#============================================================================================
# pyMagPlot.py
# 
# 
# author:           David Witten
# last modified:    02/01/2021
#============================================================================================
#from pathlib import Path
import wx

class DirTreeCtrl(wx.TextDropTarget):
    def __init__(self, object):

        wx.TextDropTarget.__init__(self)
        self.object = object
        
    def OnDropText(self, x, y, data):

        self.object.InsertItem(0, data)
        return True


