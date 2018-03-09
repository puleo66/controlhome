__author__ = 'Puleo'

import wx
import copy
import watching_pipe_gui

class WatchingPipeAi(object):

    def __init__(self, parent):

        self.parent = parent

        self.xend = 0
        self.yend = 0

        self.dialogLoad = True
        self.pipeDrawEnd = True

        self.redPipes = [ ( 235, 150, 128, 150 ), # 0. Horizontal pipe III.-1/3.( row )
                          ( 245, 150, 345, 150 ), # 1. Horizontal pipe III.-2/3.( row )
                          ( 355, 150, 448, 150 ), # 2. Horizontal pipe III.-3/3.( row )

                          ( 128, 480, 235, 480 ), # 3. Horizontal pipe I.-1/2.( row )
                          ( 245, 480, 348, 480 ), # 4. Horizontal pipe I.-2/2.( row )

                          ( 240, 480, 240, 315 ), # 5. Vertical pipe I-III. 1/2.
                          ( 240, 305, 240, 149 ), # 6. Vertical pipe I-III. 2/2.

                          ( 240, 310, 345, 310 ), # 7. Horizontal pipe II.-1/3.( row )
                          ( 355, 310, 445, 310 ), # 8. Horizontal pipe II.-2/3.( row )
                          ( 455, 310, 548, 310 ), # 9. Horizontal pipe II.-3/3.( row )

                          ( 122, 150, 122, 100 ), # 10. Three line(vertical)
                          ( 350, 150, 350, 100 ), # 11.
                          ( 455, 150, 455, 100 ), # 12.

                          ( 350, 310, 350, 260 ), # 13. Second line(vertical)
                          ( 450, 310, 450, 260 ), # 14.
                          ( 555, 310, 555, 260 ), # 15.

                          ( 354, 480, 354, 430 ), # 16. First line(vertical)
                          ( 122, 430, 122, 480 )  # 17. Heater line(vertical)
        ]

        self.bluePipes = [ ( 150, 130, 265, 130 ),  # 0. Horizontal pipe III.-1/3.( row )
                           ( 320, 130, 275, 130 ),  # 1. Horizontal pipe III.-2/3.( row )
                           ( 420, 130, 330, 130 ),  # 2. Horizontal pipe III.-3/3.( row )

                           ( 265, 460, 150, 460 ),  # 3. Horizontal pipe I.-1/2.( row ) (only Draw)
                           ( 320, 460, 275, 460 ),  # 4. Horizontal pipe I.-2/2.( row )

                           ( 270, 295, 270, 460 ),  # 5. Long vertical pipe I-III. 1/2.
                           ( 270, 129, 270, 285 ),  # 6. Long vertical pipe I-III. 2/2.

                           ( 320, 290, 269, 290 ),  # 7. Horizontal pipe II.-1/3.( row )
                           ( 420, 290, 330, 290 ),  # 8. Horizontal pipe II.-2/3.( row )
                           ( 520, 290, 430, 290 ),  # 9. Horizontal pipe II.-3/3.( row )

                           ( 145, 100, 145, 130 ),  # 10. Three line(vertical)
                           ( 325, 100, 325, 130 ),  # 11.
                           ( 428, 100, 428, 130 ),  # 12.

                           ( 325, 260, 325, 290 ),  # 13. Second line(vertical)
                           ( 425, 260, 425, 290 ),  # 14.
                           ( 525, 260, 525, 290 ),  # 15.

                           ( 325, 430, 325, 460 ),  # 16. First line(vertical)
                           ( 145, 460, 145, 430 )   # 17. Heater line(vertical)
        ]

        self.bluePipesSub = [ ( 270, 145 ),   # 05. +y
                              ( 270, 305 ),   # 06. +y
                              ( 245, 460 ),   # 03. -x
                              ( 355, 130 ),   # 02. -x
                              ( 355, 290 ),   # 08. -x
                              ( 455, 290 )    # 09. -x
        ]
        # pipes map to Dialogs
        self.map = [ ( 17, 3, 5, 6, 1, 11 ),
                     ( 17, 3, 5, 6, 1, 2, 12 ),
                     ( 17, 3, 5, 7, 13 ),
                     ( 17, 3, 5, 7, 8, 14 ),
                     ( 17, 3, 5, 7, 8, 9, 15 ),
                     ( 17, 3, 4, 16 ),
                     ( 17, 3, 5, 6, 0, 10 )
        ]

        # 0 = empty, 1 = fill, 2 = red run
        self.pipesFlagR = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

        # 0 = empty, 1 = fill, 2 = blue run
        self.pipesFlagB = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

        self.pipesSum = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

        self.lastDialogs = [ 0, 0, 0, 0, 0, 0, 0 ]

        self.rtemp = [ ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ),
                       ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ),
                       ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ),
                       ( 0,0 ), ( 0,0 ), ( 0,0 )
        ]

        self.btemp = [ ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ),
                       ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ),
                       ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ), ( 0,0 ),
                       ( 0,0 ), ( 0,0 ), ( 0,0 )
        ]

        self.pipes = watching_pipe_gui.WatchingPipe(self)

    def DispatchDrawPipes(self, dc, dialogs):

        self.pipes.InstallPipes(dc, self.bluePipes)
        self.pipes.InstallPipes(dc, self.redPipes)

        if self.dialogLoad:
            self.CheckDialogsSum(dialogs)
            self.CheckDialog(dialogs)

            self.ret0R, self.ret1R, self.ret2R = self.CheckPipesMap(self.pipesFlagR)
            self.ret0B, self.ret1B, self.ret2B = self.CheckPipesMap(self.pipesFlagB)

        self.CheckFillPipes(dc, self.ret1R, self.redPipes, wx.RED)
        self.CheckFillPipes(dc, self.ret1B, self.bluePipes, wx.BLUE)

        self.CheckRunPipe(dc, self.ret2R, self.redPipes, wx.RED, self.rtemp, self.pipesFlagR)
        self.CheckRunPipe(dc, self.ret2B, self.bluePipes, wx.BLUE, self.btemp, self.pipesFlagB)

        if len(self.ret2R) == 0:
            if len(self.ret2B) == 0:
                self.pipeDrawEnd = False                    # Main.py  - disable updating

    def CheckRunPipe(self, dc, switch, map, color, buffer, flag):

        if len(switch) != 0:
            self.pipes.DrawSetColor(dc, 1, color)
            nr = switch[0]

            x0 = map[nr][0]
            y0 = map[nr][1]
            x1 = map[nr][2]
            y1 = map[nr][3]

            if buffer[nr][0] == 0 & buffer[nr][1] == 0:
                if x0 < x1:
                    self.xend = x1
                    self.sw = 0
                    x, y = self.pipes.DrawColorPipe(dc, x0, x0+1, y0, y1)

                if x0 > x1:
                    self.xend = x1
                    self.sw = 1
                    x, y = self.pipes.DrawColorPipe(dc, x0, x0-1, y0, y1)

                if y0 < y1:
                    self.yend = y1
                    self.sw = 2
                    x, y = self.pipes.DrawColorPipe(dc, x0, x1, y0, y0+1)

                if y0 > y1:
                    self.yend = y1
                    self.sw = 3
                    x, y = self.pipes.DrawColorPipe(dc, x0, x1, y0, y0-1)

                self.listToTupes(nr,buffer, x, y)

            else:

                x0temp = buffer[nr][0]
                y0temp = buffer[nr][1]

                x, y = self.pipes.DrawColorPipe(dc, x0, x0temp, y0, y0temp)

                if x == x1:

                    self.DispSwitch(self.sw, nr, x, y, self.yend, buffer, flag)

                if y == y1:

                    self.DispSwitch(self.sw, nr, x, y, self.xend, buffer, flag)

    def DispSwitch(self, sw, nr, x, y, end, buffer, flag):
        if sw == 0:
            if x <= end:
                self.DispIf(True, nr, buffer, flag, x, y)
            else:
                self.DispIf(False, nr, buffer, flag, x, y)

        if sw == 1:
            if x >= end:
                self.DispIf(True, nr, buffer, flag, x, y)
            else:
                self.DispIf(False, nr, buffer, flag, x, y)

        if sw == 2:
            if y <= end:
                self.DispIf(True, nr, buffer, flag, x, y)
            else:
                self.DispIf(False, nr, buffer, flag, x, y)

        if sw == 3:
            if y >= end:
                self.DispIf(True, nr, buffer, flag, x, y)
            else:
                self.DispIf(False, nr, buffer, flag, x, y)

    def DispIf(self,sw, nr, buffer, flag, x, y):
        if sw:
            self.listToTupes(nr,buffer, x, y)

        else:
            self.listToTupes(nr,buffer, 0, 0)
            flag[nr] = 1
            self.dialogLoad = True

    def listToTupes(self, nr, Slist, x, y):

        Slist[nr] = list(Slist[nr])
        Slist[nr][0] = x
        Slist[nr][1] = y
        Slist[nr] = tuple(Slist[nr])

    def CheckDialogsSum(self, dialogs):
        if dialogs != self.lastDialogs:

            for nr in range(len(dialogs)):
                if dialogs[nr] > self.lastDialogs[nr]:
                    if dialogs[nr] != 1:
                        self.DialogsSubSum(nr, True)

                if dialogs[nr] < self.lastDialogs[nr]:
                    self.DialogsSubSum(nr, False)

                self.ClearColorPipes()

            self.lastDialogs = copy.copy(dialogs)

    def CheckDialog(self, dialogs):

        for nr in range(len(dialogs)):
            if dialogs[nr] == 2:
                mapTmpR = self.map[nr]
                mapLenR = len(mapTmpR)
                for pipetmpR in range(mapLenR):
                    nr0 = self.pipesFlagR[mapTmpR[pipetmpR]]
                    if nr0 == 0:
                        self.pipesFlagR[mapTmpR[pipetmpR]] = 2
                        self.dialogLoad = False
                        break

                    if nr0 == 2:
                        break

                    if mapLenR - 1== pipetmpR:
                        mapTmpB = list(reversed(mapTmpR))
                        for pipetmpB in range(len(mapTmpB)):
                            nr1 = self.pipesFlagB[mapTmpB[pipetmpB]]
                            if nr1 == 0:
                                self.pipesFlagB[mapTmpB[pipetmpB]] = 2
                                self.dialogLoad = False
                                break

                            if nr1 == 2:
                                break


    def CheckFillPipes(self, dc, switch, map, color):
        if len(switch) != 0:
            self.pipes.DrawSetColor(dc, 1, color)
            for i in switch:

                x0 = map[i][0]
                y0 = map[i][1]
                x1 = map[i][2]
                y1 = map[i][3]

                if self.JmpBluePipes(dc, x0, y0, x1, y1, color):
                    dc.DrawLine(x0,y0,x1,y1)

    def CheckPipesMap(self,list):

        ret0 = []
        ret1 = []
        ret2 = []

        i = 0

        for nr in list:
            if nr == 0:
                ret0.insert(i,i)
            if nr == 1:
                ret1.insert(i,i)
            if nr == 2:
                ret2.insert(i,i)
            i += 1

        return ret0, ret1, ret2

    def JmpBluePipes(self, dc, x0, y0, x1, y1, color):

        if color == wx.BLUE:
            for i in self.bluePipesSub:
                if x0 == i[0]:
                    if y0 < i[1] < y1:
                        dc.DrawLine(x0,y0,x0,i[1])
                        dc.DrawLine(x0,i[1]+10,x0,y1)
                        return False

                if y0 == i[1]:
                    if x1 < i[0] < x0:
                        dc.DrawLine(x0,y0,i[0],y0)
                        dc.DrawLine(i[0] - 10,y0,x1,y0)
                        return False

        return True

    def DialogsSubSum(self, nr , flag):
            mapTmp = self.map[nr]
            for i in range(len(mapTmp)):
                if flag:
                    self.pipesSum[mapTmp[i]] += 1
                else:
                    self.pipesSum[mapTmp[i]] -= 1

    def ClearColorPipes(self):
        for i in range(len(self.pipesSum)):
            if self.pipesSum[i] == 0:
                self.pipesFlagB[i] = 0
                self.pipesFlagR[i] = 0

