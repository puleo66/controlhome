__author__ = 'Puleo'


import wx
import heater_main

class WatchingRadiator(object):

    def __init__(self, parent, x, y, n, mirror=False, visible=False):

        self.parent = parent
        self.vis_w = 80
        self.vis_h = 80

        self.x = x
        self.y = y

        heater_main.radiators[n] = {'x': self.x, 'y': self.y}

        self.seg_x = self.x + 10
        self.seg_y = self.y + 10

        self.mirror = mirror

        self.pla_x = self.x + 16
        self.pla_y = self.y + 20
        self.pla_w = 40
        self.pla_h = 20

        self.visibl = visible
        self.addr = "0.00.0"
        self.descript = ""
        self.th_mass = "00"

    def Draw(self, dc):

        self.DefaultRadiator(dc)
        self.Plat(dc)

        if not self.visibl:
            self.Visible(dc)

    def DefaultRadiator(self, dc):
        for i in range(0, 5):
            self.Segment(dc, i*13)

        self.Closing(dc)


    def Segment(self, dc, n):
        pen1 = wx.Pen('#404040', 12, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        dc.DrawLine(self.seg_x+n, self.seg_y, self.seg_x+n, self.seg_y+50)

        pen1 = wx.Pen('#707070', 6, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        dc.DrawLine(self.seg_x+n, self.seg_y, self.seg_x+n, self.seg_y+50)

        pen1 = wx.Pen('#a0a0a0', 1, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        dc.DrawLine(self.seg_x+n, self.seg_y, self.seg_x+n, self.seg_y+50)

    def Closing(self, dc):

        if self.mirror:
            dc.GradientFillLinear((self.seg_x-12, self.seg_y+2, 5, 10), '#404040', '#a0a0a0', wx.SOUTH)
            dc.GradientFillLinear((self.seg_x-12, self.seg_y+39, 5, 10), '#404040', '#a0a0a0', wx.NORTH)
        else:
            dc.GradientFillLinear((self.seg_x+(5*13)-6, self.seg_y+2, 5, 10), '#404040', '#a0a0a0', wx.SOUTH)
            dc.GradientFillLinear((self.seg_x+(5*13)-6, self.seg_y+39, 5, 10), '#404040', '#a0a0a0', wx.NORTH)

    def Plat(self, dc):
        background = wx.Colour(0, 0, 0)
        dc.SetBrush(wx.Brush(background))
        dc.DrawRectangle(self.pla_x, self.pla_y, self.pla_w, self.pla_h)

        if self.visibl:
            tw, th = dc.GetTextExtent(self.th_mass + '%')
            dc.SetTextForeground(wx.WHITE)
            dc.DrawText(self.th_mass + '%', self.pla_x+(self.pla_w-tw)/2, self.pla_y+(self.pla_h-th)/2)

    def Visible(self, dc):

        dc.SetBrush(wx.Brush('#303030', wx.CROSSDIAG_HATCH))
        dc.DrawRectangle(self.x - 5, self.y, self.vis_w, self.vis_h)
