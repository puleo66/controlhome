#!/usr/bin/env python
__copyright__ = "Copyright (C) 2017 Csaba Pál - Released under terms of the AGPLv3 License"

from time import localtime, strftime

import wx
import wx.lib.agw.aui as aui
import serial

import comm_thread
import options as optBtn
import options_comm
import options_system
import options_fht
import options_termo
import heater_main
import heater_doors
import heater_log


ID_TIMER = 100

class MainFrame(wx.Frame):


    """Constructor"""
    def __init__(self):
         #Create a master window
        wx.Frame.__init__(self, None, title="ControlHome 1.06", size=(1024, 768))
        self.SetBackgroundColour("WHEAT")

        self.timer=wx.Timer(self, ID_TIMER)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_TIMER, self.TimerEvent, self.timer)

        self.serial = serial.Serial()
        self.commthread = comm_thread.CommThread(self.serial)

        self.fhtTread = False
        self.message_prev =""

        self.logCount = 0
        self.headerCount = 0

        self.CreateNotebook()
        self.notebook.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnNoteBookChanged)


        self.notebook.EnableTab(0, False)
        self.notebook.EnableTab(1, True)
        self.notebook.SetSelection(1)

        self.sb = self.CreateStatusBar(2)
        self.sb.SetForegroundColour(wx.RED)
        self.sb.SetStatusText(strftime("%Y-%m-%d   %H:%M", localtime())[2:])
        self.timeCount = 0

        self.Centre()
        self.Layout()
        self.Refresh(True)


    # Functions
    def OnExit(self,e):
        self.self.commthread.stop()               # stop reader thread
        self.serial.close()                       # cleanup
        self.Close(True)                          # Close the frame.
        e.Skip()

    def OnClose(self,e):
        dlg = wx.MessageDialog(self,
        "Do you really want to close this application ?",
        "Confirm Close", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()

        if result == wx.ID_OK:
            self.Destroy()

    def CreateNotebook(self):

        style = aui.AUI_NB_DEFAULT_STYLE ^ aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
        self.notebook = aui.AuiNotebook(self, agwStyle=style)

# Heating page !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        self.heating_window = wx.SplitterWindow(self.notebook)
        self.heating_windowSub = wx.SplitterWindow(self.heating_window)

        self.notebook.AddPage(self.heating_window, 'Heating', False)

        self.paintPanel = heater_main.HeaterPanel(self.heating_window)
        self.paintPanelDoors = heater_doors.HeaterPanelDoors(self.heating_windowSub)
        self.logPanel = heater_log.HeaterLogPanel(self.heating_windowSub)

        self.heating_windowSub.SplitHorizontally(self.paintPanelDoors, self.logPanel)
        self.heating_windowSub.SetSashGravity(0.42)

        self.heating_window.SplitVertically(self.paintPanel, self.heating_windowSub)
        self.heating_window.SetSashGravity(0.83)

        self.Layout()

# Options page !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        self.option_window = wx.SplitterWindow(self.notebook)
        self.notebook.AddPage(self.option_window, 'Options', False)

        self.leftPanel = optBtn.CntrBtnPnl(self.option_window)
        self.rightPanel0 = options_comm.Connection(self.option_window, self.serial, self.commthread)
        self.rightPanel1 = options_system.System(self.option_window, self.commthread)
        self.rightPanel2 = options_fht.Fht80(self.option_window, self.commthread)
        self.rightPanel3 = options_termo.Termo(self.option_window)

        self.optionPnlChange(0)

# Begin Options page setup ###################################################################################################

    def OpPanelHide(self):
        self.rightPanel0.Hide()
        self.rightPanel1.Hide()
        self.rightPanel2.Hide()
        self.rightPanel3.Hide()

    def optionPnlChange(self, nr):
        if(nr == 0):
            self.fhtTread = False
            self.OpPanelHide()
            self.option_window.SplitVertically(self.leftPanel, self.rightPanel0)
            self.rightPanel0.Show()

        if(nr == 1):
            self.fhtTread = False
            self.OpPanelHide()
            self.option_window.Unsplit()
            self.option_window.SplitVertically(self.leftPanel, self.rightPanel1)
            self.rightPanel1.load()
            self.rightPanel1.Show()

        if(nr == 2):
            self.OpPanelHide()
            self.option_window.Unsplit()
            self.option_window.SplitVertically(self.leftPanel, self.rightPanel2)
            self.fhtTread = True
            self.rightPanel2.load()
            self.rightPanel2.Show()

        if(nr == 3):
            self.OpPanelHide()
            self.option_window.Unsplit()
            self.option_window.SplitVertically(self.leftPanel, self.rightPanel3)
            self.rightPanel3.Show()

        self.option_window.SetSashPosition(100)
        self.Layout()

    def disableOpPanelBtn(self):
        self.leftPanel.btnSys.Disable()
        self.leftPanel.btnFht.Disable()

        self.notebook.EnableTab(0, False)  # Tab 0 Disabled

    def enableOpPanelBtn(self):
        self.leftPanel.btnSys.Enable()
        self.leftPanel.btnFht.Enable()

        self.notebook.EnableTab(0, True)   # Tab 0 Enabled
# End Options page setup ###############################################################################################

# NoteBook Setup #######################################################################################################
    def OnNoteBookChanged(self, evt):
        cp = evt.Selection

        if cp == 0:
            self.subTimer()
            self.paintPanel.paint.Refresh()

            self.timer.Start(500)  # 500 msec

        if cp == 1:
            self.timer.Stop()

        evt.Skip()

# End NoteBook setup ###################################################################################################

    def subTimer(self):
        val0 = self.commthread.dispath(True, 'H')
        val1 = self.commthread.dispath(True, 'E')

        self.paintPanel.paint.HeaterMain(self.rightPanel3, val0, val1)

# Timer Event !#########################################################################################################
    def TimerEvent(self, event):
        self.logCount += 1
        self.headerCount += 1
        self.timeCount += 1
#-----------------------------------------------------------------------------------------------------------------------
        if self.logCount >= 5:   # 2.5 sec

            self.logCount = 0
            val  = self.commthread.dispath(True, 'L')

            if self.message_prev != val:

                # Log Panel
                self.logPanel.load(strftime("%Y-%m-%d %H:%M", localtime())[2:]+ val)
                self.message_prev = val

                # Door Panel
                self.paintPanelDoors.paint.CheckDoor(val)
#-----------------------------------------------------------------------------------------------------------------------
        # Heater Panel
        if self.headerCount >= 240:                     # Update 2 minute !!!
            #val0 = self.commthread.dispath(True, 'H')
            #val1 = self.commthread.dispath(True, 'E')
            #self.paintPanel.paint.HeaterMain(self.rightPanel3, val0, val1)

            self.subTimer()
            self.headerCount = 0
        else:
            if self.paintPanel.paint.pipes.pipeDrawEnd:
                self.headerCount = 0
                self.paintPanel.paint.Refresh()

        if self.timeCount > 2:
            self.sb.SetStatusText(strftime("%Y-%m-%d   %H:%M", localtime())[2:])
            self.timeCount = 0


        event.Skip()
#-----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
     app = wx.App()
     MainFrame().Show()
     app.MainLoop()