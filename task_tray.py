# -*- encoding: utf-8 -*-
import wx,os,sys

class MyTxtCtr(wx.PySimpleApp):
    
    def OnInit(self):
        argvs = sys.argv

        instance_name = u"%s-%s" % (self.GetAppName(), wx.GetUserId())
        self.instance = wx.SingleInstanceChecker(instance_name)
        if self.instance.IsAnotherRunning():
            wx.Exit()

        self.tb_ico=wx.TaskBarIcon()
        self.tb_ico.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTbiLeftDClick)
        self.tb_ico.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.OnTbiRightUp)
        self.ico = wx.Icon("homu.ico", wx.BITMAP_TYPE_ICO)
        self.tb_ico.SetIcon(self.ico, u"homuhomu")

        self.menu = wx.Menu()
        self.menu.Append(1,   u"Exit(&X)")
        wx.EVT_MENU(self.menu, 1, self.OnClose)

        self.Frm = wx.Frame(None, -1, "homuLauncher", size=(400,60),pos=(400,400))
        self.TxtCtr = wx.TextCtrl(self.Frm, -1)
        self.Frm.Show()
        return 1

    def OnTbiLeftDClick(self, evt):
        if self.Frm.IsShown():
            self.Frm.Show(False)
        else:
            self.Frm.Show()
            self.Frm.Raise()
            
    def OnTbiRightUp(self, evt):
        self.tb_ico.PopupMenu(self.menu)

    def OnClose(self, evt):
        self.tb_ico.RemoveIcon()
        wx.Exit()

app = MyTxtCtr()
app.MainLoop()




