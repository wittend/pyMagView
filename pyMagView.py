#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.1 on Mon Feb 15 11:29:33 2021
#

# This is an automatically generated file.
# Manual changes will be overwritten without warning!

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
