__author__ = 'Puleo'

import wx
import wx.grid

SHOW_TASK = 1 << 0
SHOW_HEX  = 1 << 1

SHOW_ALL = SHOW_TASK | SHOW_HEX

class System(wx.Panel):

    def __init__(self, parent, thread):
        self.parent = parent
        self.thread = thread
        self.show = SHOW_ALL
        self.gridRow = 0

        wx.Panel.__init__(self, parent = parent)

        self.label_addr0 = wx.StaticText(self, -1, "Address:")
        self.lst = wx.ListBox(self, -1, choices = [], style = wx.LB_SINGLE)
        self.label_data0 = wx.StaticText(self, -1, "Task name:")
        self.data_name = wx.StaticText(self, -1, "Valami0")
        self.label_data1 = wx.StaticText(self, -1, "Prio:")
        self.data_prio = wx.StaticText(self, -1, "Valami1")
        self.label_data2 = wx.StaticText(self, -1, "Task status:")
        self.data_status = wx.StaticText(self, -1, "Valami2")
        self.label_data3 = wx.StaticText(self, -1, "Pointer:")
        self.data_pointer = wx.StaticText(self, -1, "Valami3")
        self.label_data4 = wx.StaticText(self, -1, "Timeout:")
        self.data_timeout = wx.StaticText(self, -1, "Valami4")
        self.label_data5 = wx.StaticText(self, -1, "ExecTime:")
        self.data_exectime = wx.StaticText(self, -1, "Valami5")
        self.label_data6 = wx.StaticText(self, -1, "Num. Act:")
        self.data_numact = wx.StaticText(self, -1, "Valami6")
        self.label_data7 = wx.StaticText(self, -1, "Stack Addr:")
        self.data_stack_addr = wx.StaticText(self, -1, "Valami7")
        self.label_data8 = wx.StaticText(self, -1, "Stack Bytes:")
        self.data_stack_bytes = wx.StaticText(self, -1, "Valami8")
        self.sizer_task_staticbox = wx.StaticBox(self, -1, "Tasks")

        self.panel_hex = wx.Panel(self, -1)
        self.hex_grid = wx.grid.Grid(self.panel_hex, -1)
        self.sizer_hex_staticbox = wx.StaticBox(self.panel_hex, -1, "Stack Memory")



        self.__set_properties()
        self.__do_layout()


        # attach the event handlers
        self.__attach_events()


    def __set_properties(self):
        if self.show & SHOW_TASK:
            self.data_name.SetLabel("")
            self.data_prio.SetLabel("")
            self.data_status.SetLabel("")
            self.data_pointer.SetLabel("")
            self.data_timeout.SetLabel("")
            self.data_exectime.SetLabel("")
            self.data_numact.SetLabel("")
            self.data_stack_addr.SetLabel("")
            self.data_stack_bytes.SetLabel("")

        if self.show & SHOW_HEX:
            self.hex_grid.CreateGrid(1, 17)
            self.defaultGrid()



    def __do_layout(self):

        self.sizer_task_staticbox.Lower()
        sizer_task = wx.StaticBoxSizer(self.sizer_task_staticbox, wx.VERTICAL)

        self.sizer_hex_staticbox.Lower()
        sizer_hex = wx.StaticBoxSizer(self.sizer_hex_staticbox, wx.VERTICAL)

        sizer_win = wx.BoxSizer(wx.VERTICAL)

        gbs = wx.GridBagSizer(4,0)

        gbs.Add(self.label_addr0, (0,0))
        gbs.Add(self.lst, (1,0), span=(10,1), flag=wx.EXPAND)

        gbs.Add(self.label_data0, (1,3))
        gbs.Add(self.data_name, (1,6))
        gbs.Add(self.label_data1, (2,3))
        gbs.Add(self.data_prio, (2,6))
        gbs.Add(self.label_data2, (3,3))
        gbs.Add(self.data_status, (3,6))
        gbs.Add(self.label_data3, (4,3))
        gbs.Add(self.data_pointer, (4,6))
        gbs.Add(self.label_data4, (5,3))
        gbs.Add(self.data_timeout, (5,6))
        gbs.Add(self.label_data5, (6,3))
        gbs.Add(self.data_exectime, (6,6))
        gbs.Add(self.label_data6, (7,3))
        gbs.Add(self.data_numact, (7,6))
        gbs.Add(self.label_data7, (8,3))
        gbs.Add(self.data_stack_addr, (8,6))
        gbs.Add(self.label_data8, (9,3))
        gbs.Add(self.data_stack_bytes, (9,6))


        sizer_task.Add(gbs, 0, flag=wx.ALL, border=5)
        sizer_win.Add(sizer_task, 0, wx.EXPAND, 0)

        sizer_hex.AddSpacer(10)
        sizer_hex.Add(self.hex_grid, 0, wx.EXPAND, 10)
        self.panel_hex.SetSizer(sizer_hex)
        sizer_win.Add(self.panel_hex, 1, wx.EXPAND, 0)

        self.SetAutoLayout(True)
        self.SetSizer(sizer_win)
        sizer_win.Fit(self)
        self.Layout()


    def __attach_events(self):
        self.Bind(wx.EVT_LISTBOX, self.onListBox, self.lst)

    def onListBox(self, event):
        currLevel = self.lst.GetSelection()
        data = hex(int(self.lst.Items[currLevel]))[2:]

        self.loadData(data)


    def load(self):

        val = self.thread.dispath(True, 'l')

        self.lst.Clear()

        for i in val:
            self.lst.Append(val[i])

        self.lst.Select(0)

        """ Refresh Task """

        currLevel = self.lst.GetSelection()
        data = hex(int(self.lst.Items[currLevel]))[2:]
        self.loadData(data)

        self.Layout()
        self.Fit()


    def loadData(self, data):

        wx.BeginBusyCursor()
        self.Hide()         #""" Self Panel Hide """

        self.defaultGrid()

        val = self.thread.dispath(True, 't' + data)

        self.insertStr(3, val)

        self.data_name.SetLabel(val[0])
        self.data_prio.SetLabel(val[1])
        self.data_status.SetLabel(val[2])
        self.data_pointer.SetLabel(val[3])
        self.data_timeout.SetLabel(val[4])
        self.data_exectime.SetLabel(val[5])
        self.data_numact.SetLabel(val[6])

        if self.data_status.GetLabel() == '0':
            self.loadStackAddress(data)
        else:
            self.hex_grid.ClearGrid()

        self.Show()

        wx.EndBusyCursor()

    def loadStackAddress(self, data):

        val = self.thread.dispath(True, 'T' + data)

        self.insertStr(0, val)

        self.stackBaseAddr      = val[0][1:]
        self.stackSize          = val[1][1:]
        self.stackUsesBytes     = val[2][1:]
        self.stackPointerAddr   = val[3][1:]

        self.loadAddress = int(self.stackPointerAddr, 16) - int(self.stackSize, 16)


        self.data_stack_bytes.SetLabel(val[1])
        self.data_stack_addr.SetLabel(val[3])

        while self.loadAddress != int(self.stackPointerAddr, 16):

            val_tmp = self.loadStackData(hex(self.loadAddress)[2:], '10')
            self.hex_grid.SetRowLabelValue(self.gridRow, hex(self.loadAddress)[2:].upper())

            self.codeHex(val_tmp)
            self.codeAscii(val_tmp)

            self.loadAddress += 0x10
            self.gridRow += 1
            self.hex_grid.InsertRows(self.gridRow)

        self.hex_grid.DeleteRows(self.gridRow)
        self.gridRow -= 1


    def loadStackData(self, addr, offs):

        val = self.thread.dispath(True, 'b' + addr + offs)
        return val

    def defaultGrid(self):
        if self.gridRow > 0:
            self.hex_grid.DeleteRows(0,self.gridRow,True)
            self.gridRow = 0


        for i in range(16):
            #self.hex_grid.SetColSize(i, 25)  // PC- hex byte
            self.hex_grid.SetColSize(i, 37)

        for i in range(16):
            self.hex_grid.SetColLabelValue(i, '0' + hex(i)[2:].upper())

        ascii_chr = ''
        for i in range(10):
            ascii_chr +=  chr(0x30 + i)

        for i in range(6):
            ascii_chr +=  chr(0x41 + i)

        #self.hex_grid.SetColSize(16, 128)  //  PC- ascii panel
        self.hex_grid.SetColSize(16, 160)
        self.hex_grid.SetColLabelValue(16, ascii_chr)

        #self.hex_grid.SetRowLabelSize(73)   // PC - Hex address
        self.hex_grid.SetRowLabelSize(91)
        self.hex_grid.SetRowLabelValue(0, "")


        self.hex_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.hex_grid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )

    def codeHex(self, tmp):
        for i in tmp:
            if(len(tmp[i]) == 2):
                self.hex_grid.SetCellValue(self.gridRow, i, '0' + tmp[i][1:])
            else:
                self.hex_grid.SetCellValue(self.gridRow, i, tmp[i][1:])

    def codeAscii(self, tmp):
        char_var = ''

        for i in range(16):
            j = int('0' + tmp[i], 16)
            if 0x00 <= j <= 0x1F:
                char_var += '?'
            elif 0x20 <= j <= 0x7F:
                char_var += chr(j)
            elif 0x80 <= j <= 0xFF:
                char_var += "."

        self.hex_grid.SetCellValue(self.gridRow, 16, char_var.upper())

    def insertStr(self, nr, var):

        for i in range(nr, len(var), 1):
            l = len(var[i])
            if l != 9:
                n = 9 - l
                k = 0
                while k != n:
                    var[i] = var[i][:1] + '0' + var[i][1:]
                    k += 1


