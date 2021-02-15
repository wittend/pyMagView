#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Modified from ZetCode wxPython tutorial

Select and parse a CSV file

author: David Witten
last modified: December 2020
"""
from pathlib import Path
import os
import wx
import sys

class DataDisplayCtrl(wx.ListCtrl):
    """
        class DataDisplayCtrl()
    """
    def __init__(self, parent, data):
        """
            __init__()
        """
        super(DataDisplayCtrl, self).__init__()
        self.InitUI(parent)
        
        
    def InitUI(self, parent):
        self.dataCtrl = wx.ListCtrl.__init__(
                self,
                parent,
                -1,
                style= wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES
            )
        # self.fileReader = SWxLogFileReader(parent)
        self.SetBackgroundColour("white")
        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("#d5ffb0")
        self.attr2 = wx.ListItemAttr()
        self.attr2.SetBackgroundColour("#ededed")
        #self.SetItemCount(len(data))
        
    def OnGetItemAttr(self, item):
        """
            OnGetItemAttr()
        """
        if item % 2 == 1:
            return self.attr1
        else:
            return self.attr2

    def OnGetItemText(self, item, col):
        """
            OnGetItemText(()
            Required for virtual: return contents cell as string
        """
        items = (self.items[item][col])
        return str(items)

    def GetColumnHeaders(self):
        """
            GetColumnHeaders()
            Return a list of columns
        """
        return self.col
    
    def makeBlank(self):
        """
            makeBlank()
        """
        empty = wx.Bitmap(16,16,32)
        dc = wx.MemoryDC(empty)
        dc.SetBackground(wx.Brush((0,0,0,0)))
        dc.Clear()
        del dc
        empty.SetMaskColour((0,0,0))
        return empty

    def OnItemSelected(self, event):
        """
            OnItemSelected()
        """
        self.currentItem = event.Index

    def OnItemActivated(self, event):
        """
            OnItemActivated()
        """
        self.currentItem = event.Index

    def getColumnText(self, index, col):
        """
            getColumnText()
        """
        item = self.GetItem(index, col)
        return item.GetText()
