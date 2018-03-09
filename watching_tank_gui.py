__author__ = 'Puleo'


import wx

class WatchingTank(object):

    def __init__(self, parent, x, y):

        self.parent = parent
        self.w = 100
        self.h = 150

        self.x = x
        self.y = y

        #self.pla_x = self.x + 30
        self.pla_x = self.x + 20
        self.pla_y = self.y + 30
        #self.pla_w = 40
        self.pla_w = 60
        self.pla_h = 20

        #self.th_mass0 = "--"
        #self.th_mass1 = "--"
        self.Hot_Water_Top = "--"
        self.Hot_Water_Bottom = "--"

        #self.address0 = ""
        #self.address1 = ""

    def InstallTank(self, dc):

        self.Roof(dc, self.y + self.h + 4)
        self.Roof(dc, self.y)
        self.Cylinder(dc)
        self.Plat(dc)
        self.Closing(dc, self.x + self.w + 10, self.y + 15)
        self.Closing(dc, self.x + self.w + 10, self.y + 105)

    def Plat(self, dc):

        pen1 = wx.Pen('#404040', 2, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        background = wx.Colour(0, 0, 0)
        dc.SetBrush(wx.Brush(background))
        dc.DrawRectangle(self.pla_x, self.pla_y, self.pla_w, self.pla_h)

        tw, th = dc.GetTextExtent(self.Hot_Water_Top + ' °C')
        dc.SetTextForeground(wx.WHITE)
        dc.DrawText(self.Hot_Water_Top + ' °C', self.pla_x+(self.pla_w-tw)/2, self.pla_y+(self.pla_h-th)/2)

        background = wx.Colour(0, 0, 0)
        dc.SetBrush(wx.Brush(background))
        dc.DrawRectangle(self.pla_x, self.pla_y + 90, self.pla_w, self.pla_h)

        tw, th = dc.GetTextExtent(self.Hot_Water_Bottom + ' °C')
        dc.SetTextForeground(wx.WHITE)
        dc.DrawText(self.Hot_Water_Bottom + ' °C', self.pla_x+(self.pla_w-tw)/2, self.pla_y + 90 +(self.pla_h-th)/2)


    def Cylinder(self, dc):

        dc.GradientFillLinear((self.x - 10, self.y, 40, self.h + 1), '#404040', '#707070', wx.EAST)
        dc.GradientFillLinear((self.x + 70, self.y, 40, self.h + 1), '#404040', '#707070', wx.WEST)

        dc.GradientFillLinear((self.x + 30, self.y, 20, self.h + 1), '#707070', '#a0a0a0', wx.EAST)
        dc.GradientFillLinear((self.x + 50, self.y, 20, self.h + 1), '#707070', '#a0a0a0', wx.WEST)

    def Roof(self, dc, y):
        dc.SetBrush(wx.Brush('#404040', wx.SOLID))


        pen1 = wx.Pen('#404040', 1, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        dc.DrawEllipse(self.x-10, y - 17, self.w + 19, 30)

    def Closing(self, dc, x, y):

        dc.GradientFillLinear((x, y, 5, 10), '#404040', '#a0a0a0', wx.SOUTH)
        dc.GradientFillLinear((x, y + 39, 5, 10), '#404040', '#a0a0a0', wx.NORTH)