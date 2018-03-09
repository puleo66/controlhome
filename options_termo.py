__author__ = 'Puleo'

import wx
import wx.grid
import configparser
import codecs

import get_temp


SHOW_SCAN = 1 << 0
SHOW_TEST  = 1 << 1
SHOW_BUTTON  = 1 << 1

SHOW_ALL = SHOW_SCAN | SHOW_TEST | SHOW_BUTTON

ID_TIMER = 100

class Termo(wx.Panel):

    def __init__(self, parent):
        self.parent = parent
        self.show = SHOW_ALL
        self.choices = ['', 'Flow Hot Water', 'Return Cold Water', 'Hot Water Top', 'Hot Water Bottom']
        self.addrCount = 0
        self.testCount = 0

        self.valTemp = {}
        self.TermoEnable = False

        wx.Panel.__init__(self, parent = parent)

        self.termo_grid = wx.grid.Grid(self, -1)
        self.scanButton = wx.Button(self, -1, label="", size= (40, 28))
        self.clearButton = wx.Button(self, -1, label="", size= (40, 28))
        self.saveButton = wx.Button(self, -1, label="", size= (40, 28))
        self.loadButton = wx.Button(self, -1, label="", size= (40, 28))
        self.sizer_DefStBox = wx.StaticBox(self, -1, "Temperature Sensors")

        self.panelTest = wx.Panel(self, -1)
        self.test_grid = wx.grid.Grid(self.panelTest, -1)
        self.testButton = wx.Button(self.panelTest, label="", size=(55, 28))
        self.sizer_Test_staticbox = wx.StaticBox(self.panelTest, -1, "Temperature Sensors Test")

        self.__set_properties()
        self.__do_layout()


        # attach the event handlers
        self.__attach_events()

        self.configThermo = configparser.ConfigParser()
        # Open the file with the correct encoding
        with codecs.open('/home/pi/controlhome/config_term.ini', 'r', encoding='utf-8') as f:
            self.configThermo.read_file(f)


    def __set_properties(self):
        if self.show & SHOW_SCAN:
            self.termo_grid.CreateGrid(5,2)
            self.default_ScanGrid()

        if self.show & SHOW_TEST:
            self.test_grid.CreateGrid(5, 3)
            self.defaultTestGrid()

        if self.show & SHOW_BUTTON:
            self.scanButton.SetLabelText("Scan")
            self.clearButton.SetLabelText("Clear")
            self.saveButton.SetLabelText("Save")
            self.loadButton.SetLabelText("Load")

            self.testButton.SetLabelText("Test")

            self.clearButton.Disable()
            self.saveButton.Disable()
            self.loadButton.Disable()

            self.testButton.Disable()

    def __do_layout(self):

        self.sizer_DefStBox.Lower()
        sizer_scan = wx.StaticBoxSizer(self.sizer_DefStBox, wx.VERTICAL)
        self.sizer_Test_staticbox.Lower()
        sizer_test = wx.StaticBoxSizer(self.sizer_Test_staticbox, wx.VERTICAL)

        sizer_win = wx.BoxSizer(wx.VERTICAL)

        gbs_scan = wx.GridBagSizer(0,0)
        gbs_scan.Add(self.termo_grid, (1,0), span=(7,1))
        gbs_scan.Add(self.scanButton, (1,2))
        gbs_scan.Add(self.clearButton, (1,3), span=(7,1))
        gbs_scan.Add(self.saveButton, (1,4))
        gbs_scan.Add(self.loadButton, (1,5), span=(7,1))

        sizer_scan.AddSpacer(10)
        sizer_scan.Add(gbs_scan, 0, flag=wx.ALL, border=5)
        sizer_scan.AddSpacer(10)

        sizer_win.AddSpacer(10)
        sizer_win.Add(sizer_scan, 0, wx.EXPAND, 0)

        gbs_test = wx.GridBagSizer(0,0)
        gbs_test.Add(self.test_grid, (1,0), span=(7,1))
        gbs_test.Add(self.testButton, (1,5))

        sizer_test.AddSpacer(10)
        sizer_test.Add(gbs_test, 0, flag=wx.ALL, border=5)
        sizer_test.AddSpacer(10)

        self.panelTest.SetSizer(sizer_test)
        sizer_win.AddSpacer(10)
        sizer_win.Add(self.panelTest, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_win)
        self.SetAutoLayout(True)
        self.Layout()


    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.onScan, self.scanButton)
        self.Bind(wx.EVT_BUTTON, self.onClear, self.clearButton)
        self.Bind(wx.EVT_BUTTON, self.onTest, self.testButton)
        self.Bind(wx.EVT_BUTTON, self.onSave, self.saveButton)
        self.Bind(wx.EVT_BUTTON, self.onLoad, self.loadButton)

        self.termo_grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnTermoGridCellChange)


########################################################################################################################
    def default_ScanGrid(self):

        self.termo_grid.SetColSize(0, 400)
        self.termo_grid.SetColSize(1, 200)

        self.termo_grid.SetColLabelValue(0, "Address" )
        self.termo_grid.SetColLabelValue(1, "To" )

        self.termo_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.termo_grid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )


        editor = wx.grid.GridCellChoiceEditor(self.choices)

        for row in range(5):
            self.termo_grid.SetCellValue(row, 0, ' ')


        attr = wx.grid.GridCellAttr()
        attr.SetEditor(editor)

        for row in range(5):
            self.termo_grid.SetAttr(row, 1, attr)
            if row > 0:
                attr.IncRef()

    def onScan(self, event):

        self.scanButton.Disable()

        wx.BeginBusyCursor()

        x = get_temp.DS1820()
        data, addr, count = x.loadDataTemp()

        self.addrCount = count

        for row in range(count):
            self.termo_grid.SetCellValue(row, 0, addr[row])
            self.test_grid.SetCellValue(row, 0, addr[row])
            self.test_grid.SetCellValue(row, 1, str(data[row]))


        wx.EndBusyCursor()

        self.clearButton.Enable()
        self.loadButton.Enable()
        self.testButton.Enable()

        event.Skip()

    def onClear(self, event):

        self.termo_grid.ClearGrid()
        self.test_grid.ClearGrid()

        for row in range(5):
            self.test_grid.SetCellBackgroundColour(row, 2, wx.WHITE)

        self.scanButton.Enable()

        self.clearButton.Disable()
        self.saveButton.Disable()
        self.loadButton.Disable()

        self.testButton.Disable()
        self.TermoEnable = False

        event.Skip()

    def onSave(self, event):
        cfgfile = open('/home/pi/controlhome/config_term.ini','w')
        self.configThermo.clear()

        for row in range(self.addrCount):
            title = self.termo_grid.GetCellValue(row, 0)
            self.configThermo.add_section(title)
            self.configThermo.set(title, 'to', self.termo_grid.GetCellValue(row, 1))

        self.configThermo.write(cfgfile)
        cfgfile.close()

        self.saveButton.Disable()
        event.Skip()

    def onLoad(self, event):
        for row in range(self.addrCount):
            for methodName in self.configThermo.sections():
                if methodName == self.termo_grid.GetCellValue(row, 0):
                    value = self.configThermo.get(methodName, 'to')
                    self.termo_grid.SetCellValue(row, 1, value)
                    break

        self.setupTermGrid()
        self.TermoEnable = True

        event.Skip()

    def OnTermoGridCellChange(self, event):

        row = event.GetRow()
        col = event.GetCol()

        self.test_grid.SetCellValue(row, 2, '')

        if self.termo_grid.GetCellValue(row, col) == '':
            self.test_grid.SetCellBackgroundColour(row, 2, wx.WHITE)
            if self.testCount != 0:
                self.testCount -= 1
        else:
            self.test_grid.SetCellBackgroundColour(row, 2, wx.RED)
            self.testCount += 1
            self.saveButton.Enable()
            self.loadButton.Disable()


        if self.testCount == self.addrCount:
            self.testButton.Disable()

            # End object
            self.setupTermGrid()
            self.TermoEnable = True

        self.test_grid.ForceRefresh()

        event.Skip()

########################################################################################################################
    def defaultTestGrid(self):

        self.test_grid.SetColSize(0, 400)
        self.test_grid.SetColSize(1, 100)
        self.test_grid.SetColSize(2, 100)

        self.test_grid.SetColLabelValue(0, "Address" )
        self.test_grid.SetColLabelValue(1, "°C" )
        self.test_grid.SetColLabelValue(2, "Status" )

        self.test_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.test_grid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )

        for row in range(4):
            self.test_grid.SetCellValue(row, 0, ' ')


    def onTest(self, event):

        self.gaugeTest()

        x = get_temp.DS1820()
        data, addr, count = x.loadDataTemp()

        for i in data:
            if self.test_grid.GetCellBackgroundColour(i, 1) == wx.WHITE:
                if float(self.test_grid.GetCellValue(i, 1)) + 5.0 < data[i]:
                    self.test_grid.SetCellValue(i, 2, str(data[i]))
                    self.test_grid.SetCellBackgroundColour(i, 2, wx.GREEN)


        event.Skip()


    def gaugeTest(self):
        max = 80

        dlg = wx.ProgressDialog("Load Test Temperature...",
                               "Load test!",
                               maximum = max,
                               parent=self,
                               style = wx.PD_CAN_ABORT
                                | wx.PD_APP_MODAL
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_REMAINING_TIME
                                | wx.PD_AUTO_HIDE
                                )

        keepGoing = True
        count = 0

        while keepGoing and count < max:
            count += 1
            wx.MilliSleep(700)  # 1 minute

            if count >= max / 2:
                (keepGoing, skip) = dlg.Update(count, "Half-time!")
            else:
                (keepGoing, skip) = dlg.Update(count)


        dlg.Destroy()

    def setupTermGrid(self):

        for row in range(5):
            if self.termo_grid.GetCellValue(row, 1) != '':
                self.valTemp[row] = self.termo_grid.GetCellValue(row, 1)
