#from pathlib import Path
import wx

class DirTreeCtrl(wx.TextDropTarget):
    def __init__(self, object):

        wx.TextDropTarget.__init__(self)
        self.object = object
        
    def OnDropText(self, x, y, data):

        self.object.InsertItem(0, data)
        return True


