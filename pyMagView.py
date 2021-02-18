#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#============================================================================================
# pyMagPlot.py
# 
# This routine reads ascii file data from HamSCI DASI magnetometers (RM3100) and plot graphs. 
# 
# author:           David Witten
# last modified:    02/01/2021
#============================================================================================
import wx
from topFrame import TopFrame


class TheApp(wx.App):
    def OnInit(self):
        self.topFrame = TopFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.topFrame)
        self.topFrame.Show()
        return True

# end of class TheApp

if __name__ == "__main__":
    pyMagView = TheApp(0)
    pyMagView.MainLoop()
