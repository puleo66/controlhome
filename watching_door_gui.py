__author__ = 'Puleo'


import wx
import heater_doors

class WatchingDoor(object):

    def __init__(self, parent, n, open=False, visibl=False):

        self.parent = parent
        #self.vis_w = 200
        self.vis_w = 230
        self.vis_h = 100

        self.x = 0
        self.y = self.vis_h * n

        #heater_doors.doors[n]= {'x': self.x, 'y': self.y}
        heater_doors.doors[n]= {'y': self.y}


        self.pla_x = self.x + 40
        self.pla_y = self.y + 10
        self.pla_w = 80
        self.pla_h = 20

        #self.ker_x = self.x + 110
        #self.ker_y = self.y + 10
        self.ker_x = self.pla_x + 100
        self.ker_y = self.pla_y
        self.ker_w = 50
        self.ker_h = 65

        self.open = open
        self.visibl = visibl
        self.addr = "0.00.00.0"
        self.descript = ""

    def Draw(self, dc):

        self.DefaultDoor(dc)
        self.Plat(dc)

        if self.open:
            self.OpenDoor(dc)
        else:
            self.CloseDoor(dc)

        self.Latch(dc)

        if not self.visibl:
            self.Visible(dc)

    def DefaultDoor(self, dc):

        if self.visibl:
            if self.open:
                dc.SetBrush(wx.Brush('#cc0000', wx.SOLID))
            else:
                dc.SetBrush(wx.Brush('#66ff33', wx.SOLID))

            dc.DrawRectangle(self.x, self.y, self.vis_w, self.vis_h)

        background = wx.Colour(0, 0, 0)
        dc.SetBrush(wx.Brush(background))
        dc.DrawRectangle(self.ker_x, self.ker_y, self.ker_w, self.ker_h)

        pen = wx.Pen('#4c4c4c', 2, wx.SOLID)

        pen.SetJoin(wx.JOIN_MITER)
        dc.SetPen(pen)
        dc.DrawRectangle(self.ker_x, self.ker_y, self.ker_w, self.ker_h)

    def CloseDoor(self, dc):
        if self.visibl:
            #self.dc.SetBrush(wx.Brush('#c56c00', wx.SOLID))
            dc.SetBrush(wx.Brush('#ffffff', wx.SOLID))
            dc.DrawRectangle(self.ker_x+1, self.ker_y+1, self.ker_w-1, self.ker_h-1)

    def OpenDoor(self, dc):

        #self.dc.SetBrush(wx.Brush('#c56c00', wx.SOLID))
        dc.SetBrush(wx.Brush('#ffffff', wx.SOLID))
        dc.DrawPolygon(((self.ker_x , self.ker_y),
                             (self.ker_x + 30, self.ker_y + 10),
                             (self.ker_x + 30, self.ker_y + self.ker_h - 10),
                             (self.ker_x , self.ker_y + self.ker_h)))

    def Plat(self, dc):
        background = wx.Colour(0, 0, 0)
        dc.SetBrush(wx.Brush(background))
        dc.DrawRectangle(self.pla_x, self.pla_y, self.pla_w, self.pla_h)

        if self.visibl:
            tw, th = dc.GetTextExtent(self.descript)
            dc.SetTextForeground(wx.WHITE)
            dc.DrawText(self.descript, self.pla_x+(self.pla_w-tw)/2, self.pla_y+(self.pla_h-th)/2)

    def Latch(self, dc):
        pen1 = wx.Pen('#4c4c4c', 5, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        if self.open:
            dc.DrawLine(self.ker_x + self.ker_w - 30,
                             self.ker_y + (self.ker_h/2),
                             self.ker_x + self.ker_w - 25,
                             self.ker_y + (self.ker_h/2))
        else:
            dc.DrawLine(self.ker_x + self.ker_w - 15,
                         self.ker_y + (self.ker_h/2),
                         self.ker_x + self.ker_w - 6,
                         self.ker_y + (self.ker_h/2) )

    def Visible(self, dc):

        dc.SetBrush(wx.Brush('#4c4c4c', wx.CROSSDIAG_HATCH))
        dc.DrawRectangle(self.x, self.y, self.vis_w, self.vis_h)
