__author__ = 'Puleo'


import wx

class WatchingHeater(object):

    def __init__(self, parent, x, y):

        self.parent = parent
        self.w = 140
        self.h = 180

        self.x = x
        self.y = y

        self.pla_x = self.x + 5
        self.pla_y = self.y + 155
        #self.pla_w = 40
        self.pla_w = 60
        self.pla_h = 20

        self.onOff = False
        #self.th_mass0 = "--"
        #self.th_mass1 = "--"
        self.Flow_Hot_Water = "--"
        self.Return_Cold_Water = "--"

        #self.address0 = ""
        #self.address1 = ""

    def InstallHeater(self, dc):

        self.Chimney(dc)
        self.Box(dc)
        self.Display(dc)
        self.Plat(dc)

    def Display(self, dc):

        if self.onOff:
            pen1 = wx.Pen('#66ff33', 4, wx.SOLID)
        else:
            pen1 = wx.Pen('#cc0000', 4, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        dc.SetBrush(wx.Brush('#a0a0a0', wx.SOLID))
        dc.DrawRectangle(self.x + (self.w/3) + 5, self.y + (self.h/2), 40, 20)

    def Plat(self, dc):

        pen1 = wx.Pen('#404040', 2, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        background = wx.Colour(0, 0, 0)
        dc.SetBrush(wx.Brush(background))
        dc.DrawRectangle(self.pla_x, self.pla_y, self.pla_w, self.pla_h)

        #tw, th = dc.GetTextExtent(self.th_mass0 + ' °C')
        tw, th = dc.GetTextExtent(self.Flow_Hot_Water + ' °C')
        dc.SetTextForeground(wx.WHITE)
        #dc.DrawText(self.th_mass0 + ' °C', self.pla_x+(self.pla_w-tw)/2, self.pla_y+(self.pla_h-th)/2)
        dc.DrawText(self.Flow_Hot_Water + ' °C', self.pla_x+(self.pla_w-tw)/2, self.pla_y+(self.pla_h-th)/2)

        background = wx.Colour(0, 0, 0)
        dc.SetBrush(wx.Brush(background))
        #dc.DrawRectangle(self.pla_x+50, self.pla_y, self.pla_w, self.pla_h)
        dc.DrawRectangle(self.pla_x+70, self.pla_y, self.pla_w, self.pla_h)

        #tw, th = dc.GetTextExtent(self.th_mass1 + ' °C')
        tw, th = dc.GetTextExtent(self.Return_Cold_Water + ' °C')
        dc.SetTextForeground(wx.WHITE)
        #dc.DrawText(self.th_mass1 + ' °C', self.pla_x+50+(self.pla_w-tw)/2, self.pla_y+(self.pla_h-th)/2)
        #dc.DrawText(self.Return_Cold_Water + ' °C', self.pla_x+50+(self.pla_w-tw)/2, self.pla_y+(self.pla_h-th)/2)
        dc.DrawText(self.Return_Cold_Water + ' °C', self.pla_x+70+(self.pla_w-tw)/2, self.pla_y+(self.pla_h-th)/2)

    def Chimney(self, dc):

        pen1 = wx.Pen('#404040', 25, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        dc.DrawLine(self.x + (self.w/2), self.y-5, self.x+ (self.w/2), self.y-30)

        pen1 = wx.Pen('#707070', 18, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        dc.DrawLine(self.x + (self.w/2), self.y-5, self.x+ (self.w/2), self.y-30)

        pen1 = wx.Pen('#a0a0a0', 12, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        dc.DrawLine(self.x + (self.w/2), self.y-5, self.x+ (self.w/2), self.y-30)


    def Box(self, dc):

        pen1 = wx.Pen('#a0a0a0', 4, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        dc.SetBrush(wx.Brush('#a0a0a0', wx.SOLID))
        dc.DrawRectangle(self.x+1, self.y+1, self.w-1, self.h-1)

        pen1 = wx.Pen('#707070', 4, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

        dc.DrawLine(self.x-1, self.y-1, self.x-1, self.y-1 + self.h-2)
        dc.DrawLine(self.x-1, self.y-1, self.x-1 + self.w-2, self.y-1)





