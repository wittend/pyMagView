#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
SWxLogFileReader

Read and parse a CSV file

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
        line_count = 0
        rcol = 1
        self.fileName = logFileName
        with open(logFileName, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # line_count = 0
            # rcol = 1
            wx.SetCursor(wx.HOURGLASS_CURSOR)
            for row in csv_reader:
                if line_count == 0:
                    caption = ('Row', 'UTC Stamp', u'Remote \u00b0C', u'Local \u00b0C', 'x', 'y', 'z', 'Total Field')  # 'rx', 'ry', 'rz')
                    ddCtrl.ClearAll()
                    i = 0
                    for ccol in caption:
                        ddCtrl.InsertColumn(i, ccol, format=wx.LIST_FORMAT_CENTER , width=wx.LIST_AUTOSIZE)
                        i += 1
                    rcol = i
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
                    rcol += rcol

        ddCtrl.SetItemCount(line_count)
        ddCtrl.items = items
        wx.SetCursor(wx.NullCursor)
        wx.MessageBox(f'Processed {line_count -1} lines.', 'File Read', wx.OK|wx.CENTER)
         
    def AppendRow(row):
        #row = (line_count, r[0], r[1], r[2], r[3], r[4], r[5], r[6])             #, r8[1])  #, r9[1])
        item = row
        line_count += 1
        rcol += item.len()
        ddCtrl.Append(item)
        
        
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
