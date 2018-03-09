__author__ = 'Puleo'


import wx

class WatchingPipe(object):

    def __init__(self, parent):

        self.parent = parent

        self.xBreak = [ (240,460)]

    def InstallPipes(self, dc, table):
        for pipe in range(0, len(table), 1):
            x0 = table[pipe][0]
            y0 = table[pipe][1]
            x1 = table[pipe][2]
            y1 = table[pipe][3]

            self.DrawPipe(dc, x0, y0, x1, y1)

    def DrawSetColor(self, dc, pen, color):

        pen1 = wx.Pen(color, pen, wx.SOLID)
        pen1.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen1)

    def DrawPipe(self, dc, x1, y1, x2, y2):

        self.DrawSetColor(dc, 12, '#404040')
        dc.DrawLine(x1, y1, x2, y2)

        self.DrawSetColor(dc, 6, '#707070')
        dc.DrawLine(x1, y1, x2, y2)

        self.DrawSetColor(dc, 1, '#a0a0a0')

    def DrawColorPipe(self,dc, x0, x1, y0, y1):

            if x0 != x1:
                if x0 < x1:

                    dc.DrawLine(x0,y0,x1,y1)
                    x1 += 22

                else:

                    dc.DrawLine(x0,y0,x1,y1)
                    x1 -= 22

            else:
                if y0 < y1:

                    dc.DrawLine(x0,y0,x1,y1)
                    y1 += 22
                else:

                    dc.DrawLine(x0,y0,x1,y1)
                    y1 -= 22

            return x1, y1
