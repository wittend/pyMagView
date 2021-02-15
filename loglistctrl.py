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
import csv

class SWxLogFileReader():
    """
        SWxLogFileReader
    """
    def __init__(self):
        """
            __init__()
        """
        self.line_count = 0
        self.fileName = None
        
    def OpenLogFile(self, logFileName, ddCtrl ):
        """
            OpenLogFile()
        """
        items = []
        self.fileName = logFileName
        with open(logFileName, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            rcol = 1
            wx.SetCursor(wx.HOURGLASS_CURSOR)
            for row in csv_reader:
                if line_count == 0:
                    caption = ('Row', 'UTC Stamp', u'Remote \u00b0C', u'Local \u00b0C', 'x', 'y', 'z', 'Total Field')  # 'rx', 'ry', 'rz')
                    ddCtrl.ClearAll()
                    i = 0
                    for ccol in caption:
                        ddCtrl.InsertColumn(i, ccol, format=wx.LIST_FORMAT_CENTER , width=wx.LIST_AUTOSIZE)
                        i += 1
                    line_count += 1
                else:
                    result = row[0].rsplit(':')
                    # r1 = result[1].replace(' ',',')
                    # r1a = r1[1:]
                    # r1b = r1a.replace('Dec', '12')
                    r0 = row[0].rsplit(': ')
                    r1 = row[1].rsplit(': ')
                    r2 = row[2].rsplit(': ')
                    r3 = row[3].rsplit(': ')
                    r4 = row[4].rsplit(': ')
                    r5 = row[5].rsplit(': ')
                    r6 = row[6].rsplit(': ')
                    item = (line_count, r0[1], r1[1], r2[1], r3[1], r4[1], r5[1], r6[1])             #, r8[1])  #, r9[1])
                    items.insert(line_count-1, item)
                    line_count += 1
                    rcol += 6

        ddCtrl.SetItemCount(line_count)
        ddCtrl.items = items
        wx.SetCursor(wx.NullCursor)
        wx.MessageBox(f'Processed {line_count -1} lines.', 'File Read', wx.OK | wx.CENTER)
         

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


class TopMainFrame(wx.Frame):
    """
        class TopMainFrame()
    """
    def __init__(self, *args, **kwds):
        """
            __init__(self, *args, **kw)
        """       
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        super(TopMainFrame, self).__init__(*args, **kwds)
        self.SetSize((850, 550))
        self.SetTitle("Log File Browser")
        self.InitUI()

    def InitUI(self):
        """
            InitUI()
        """
        # Tool Bar
        self.topFrame_toolbar = wx.ToolBar(self, -1, style=wx.TB_DEFAULT_STYLE)
        tool = self.topFrame_toolbar.AddTool(wx.ID_ANY, "New", wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (24, 24)), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
#        self.Bind(wx.EVT_TOOL, self.OnFileNew, id=tool.GetId())
        tool = self.topFrame_toolbar.AddTool(wx.ID_ANY, "Open", wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (24, 24)), wx.NullBitmap, wx.ITEM_NORMAL, "Open a file", "Open a file")
#        self.Bind(wx.EVT_TOOL, self.OnFileOpen, id=tool.GetId())
        tool = self.topFrame_toolbar.AddTool(wx.ID_ANY, "Save", wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, (24, 24)), wx.NullBitmap, wx.ITEM_NORMAL, "Save current file", "")
#        self.Bind(wx.EVT_TOOL, self.OnFileSave, id=tool.GetId())
        tool = self.topFrame_toolbar.AddTool(wx.ID_ANY, "SaveAs", wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, (24, 24)), wx.NullBitmap, wx.ITEM_NORMAL, "Save Current File As", "")
#        self.Bind(wx.EVT_TOOL, self.OnFileSaveAs, id=tool.GetId())
        self.topFrame_toolbar.AddSeparator()
        self.SetToolBar(self.topFrame_toolbar)
        self.topFrame_toolbar.Realize()
        # Tool Bar end
        
        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.window_1 = wx.SplitterWindow(self.panel_1, wx.ID_ANY)
        self.window_1.SetMinimumPaneSize(20)
        sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
        self.window_1_pane_1 = wx.Panel(self.window_1, wx.ID_ANY)
        
        self.home = str(Path.home()) + "/PSWS/Srawdata"
        #dirWidget.SetDefaultPath(self.home)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.dirWidget = wx.GenericDirCtrl(self.window_1_pane_1, wx.ID_ANY, dir=self.home)
        sizer_2.Add(self.dirWidget, 1, wx.EXPAND, 0)
        self.window_1_pane_2 = wx.Panel(self.window_1, wx.ID_ANY)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        self.ddCtrl = DataDisplayCtrl(self.window_1_pane_2, data)
        sizer_3.Add(self.ddCtrl, 1, wx.EXPAND, 0)
        
        self.window_1_pane_2.SetSizer(sizer_3)
        self.window_1_pane_1.SetSizer(sizer_2)
        self.window_1.SplitVertically(self.window_1_pane_1, self.window_1_pane_2, 250)
        self.panel_1.SetSizer(sizer_1)
        
        tree = self.dirWidget.GetTreeCtrl()
        self.Layout()
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect, id=tree.GetId())

    def OnSelect(self, event):
        """
            OnSelect()
        """
        filePath = self.dirWidget.GetPath()
        if(os.path.isdir(filePath) != True):
            #print('self.dirWidget.GetPath(): ' + self.dirWidget.GetPath())
            self.ddCtrl.ClearAll()
            self.ddCtrl.DeleteAllColumns()
            fr = SWxLogFileReader()
            fr.OpenLogFile(self.dirWidget.GetPath(), self.ddCtrl)
        else:
            print('Not a file: ' + self.dirWidget.GetPath())


def main():
    """
        main()
    """
    app = wx.App()
    tf = TopMainFrame(None)
    tf.Show()
    app.MainLoop()


if __name__ == '__main__':
    """
        Begin execution here...
    """
    lfc = SWxLogFileReader()
    main()
