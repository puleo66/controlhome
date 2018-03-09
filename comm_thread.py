#!/usr/bin/env python
__copyright__ = "Copyright (C) 2017 Csaba Pál - Released under terms of the AGPLv3 License"

import threading
import serial
import wx
import base64
import queue

SD0 = 0xED
SD1 = 0x8C
ED  = 0x8D

STATE_SD0     =  0                # waiting for start first  start delimiter (SD0)
STATE_SD1     =  1                # waiting for start second start delimiter (SD1)
STATE_LEN     =  2                # waiting for len byte
STATE_DATA    =  3                # waiting for data
STATE_CHKSUM  =  4                # waiting for checksum
STATE_ED      =  5

class CommThread(object):

    def __init__(self, serial):
        self.serial = serial
        self.alive = None
        self._reader_alive = None
        self.receiver_thread = None
        self.q = queue.Queue()

        self.RxState = STATE_SD0
        self.RxRemainLen = 0
        self.RxChkSum = 0
        self.RxBuf = ""
        self.TxBuf = bytearray(128)
        self.RxBufCnt = 0
        self.RxRdIx = 0
        self.RxCtr = 0
        self.RxPktCtr = 0
        self.TxText = ""
        self.RxTmp = ""



    def _start_reader(self):
        """Start reader thread"""
        self._reader_alive = True
        self.receiver_thread = threading.Thread(target=self.reader, name='rx')
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self._reader_alive = False
        self.receiver_thread.join()

    def start(self):
        """start worker threads"""
        self.alive = True
        self._start_reader()
        self.transmitter_thread = threading.Thread(target=self.writer, name='tx')
        self.transmitter_thread.daemon = True
        self.transmitter_thread.start()

    def stop(self):
        """set flag to stop worker threads"""
        self._stop_reader()
        self.serial.close()

    def reader(self):
        try:
            while self._reader_alive:

                inp = self.serial.read(size=1) #read a byte
                if inp:
                    in_hex = hex(int.from_bytes(inp,byteorder='little'))
                    self.onRxState(int(in_hex, 16))

        except serial.SerialException as e:

            dlg = wx.MessageDialog(None, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

            self._reader_alive = False
            raise       # XXX handle instead of re-raise?

    def writer(self):

        try:
            while self.alive:
                if not self.alive:
                    break
                self.onTxState()

        except:
            self.alive = False
            raise
########################################################################################################################

    def onRxState(self, rx_data):
        self.RxCtr += 1

        if(self.RxState != STATE_DATA):
            running = True
        else:
            running = False

        if(self.RxState == STATE_SD0):
            if(rx_data == SD1):
                self.RxState = STATE_SD1
                self.rxBufClr()
                running = False

        if(self.RxState == STATE_SD1) and running :
            if(rx_data == SD0):
                self.RxState = STATE_LEN
            else:
                self.RxState = STATE_SD0

            running = False

        if(self.RxState == STATE_LEN) and running :
            if(rx_data == 0x00) or (rx_data > 128):
                self.RxState = STATE_SD0
            else:
                self.RxChkSum = rx_data
                self.RxRemainLen = rx_data - 1
                self.RxState = STATE_DATA

            running = True

        if(self.RxState == STATE_DATA) and not running :

            self.RxBuf += str(format(rx_data, 'x')).upper()
            self.RxChkSum += rx_data
            self.RxRemainLen -= 1
            if(self.RxRemainLen == 0):
                self.RxState = STATE_CHKSUM
                running = False

        if(self.RxState == STATE_CHKSUM) and running :
            if((self.RxChkSum & 0xFF) == rx_data):
                self.RxState = STATE_ED
            else:
                self.RxState = STATE_SD0

            running = False

        if(self.RxState == STATE_ED) and running :
            if(rx_data == ED):
                self.RxPktCtr += 1
                #print(self.RxBuf)
                self._reader_alive = False

                self.RxTmp = self.RxBuf.replace('2130', '00')
                self.q.put(self.RxTmp)

            self.RxState = STATE_SD0

    def rxBufClr(self):

        self.RxBufCnt = 0
        self.RxRdIx   = 0
        self.RxBuf    = ""
        self.RxTmp    = ""
        self.q.queue.clear()
########################################################################################################################

    def onTxState(self):

        self.TxBuf.clear()
        chksum = 0

        self.TxBuf.append(SD0)
        self.TxBuf.append(SD1)

        if len(self.TxText) == 1:
            chksum = self.txState(chksum, 1)

            y = ord(self.TxText)
            chksum = self.txState(chksum, y)

        else:
            chksum = self.addrString(chksum, self.TxText)

        self.TxBuf.append((0x100 - chksum) & 0xFF)

        self.TxBuf.append(ED)

        self.serial.write(self.TxBuf)
        self.serial.flush()

        self.alive = False

    def txState(self, sum, y):

        self.TxBuf.append(y)
        sum += y
        return sum

    def addrString(self, sum, txt):

        chrStr = txt[:1]
        hexStr = txt[1:]
        chrNum = int(len(chrStr) + len(hexStr)/2)

        sum = self.txState(sum, chrNum)         # cmd Length  !!
        sum = self.txState(sum, ord(chrStr))    # cmd char !!!

        for i in range(0, len(hexStr), 2):
            sum = self.txState(sum, int(hexStr[i:i+2], 16))
        return sum


########################################################################################################################

    def dispath(self, event, chr):

        return_value = {}

        if(self._reader_alive != None):
            self.stop()
            self.serial.close()

        # open port if not called on startup, open it on startup and OK too
        if event is not None:

            try:
                self.serial.open()
            except serial.SerialException as e:

                dlg = wx.MessageDialog(None, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
                
            else:
                self.TxText = chr
                self.start()                             # send the character


                while self._reader_alive:break

                txt_byte, txt_inx = self.convChr(self.q.get())

                if( txt_byte == chr.encode('ascii')[:1]):
                    if(chr.encode('ascii') == b's' ):
                        return_value = self.transmit_s(txt_inx, self.RxTmp)

                    if(chr.encode('ascii') == b'l' ):
                        return_value = self.transmit_l(txt_inx, self.RxTmp)

                    if(chr.encode('ascii') == b'f' ):
                        return_value = self.transmit_f(txt_inx, self.RxTmp)

                    if(chr.encode('ascii') == b'a' ):
                        return_value = self.transmit_a(txt_inx, self.RxTmp)

                    if(chr.encode('ascii') == b'c' ):
                        return_value = self.transmit_b(txt_inx, self.RxTmp)

                    if(chr.encode('ascii') == b'H' ):
                        return_value = self.transmit_H(txt_inx, self.RxTmp)

                    if(chr.encode('ascii') == b'E' ):
                        return_value = self.transmit_E(txt_inx, self.RxTmp)

                    if(chr.encode('ascii') == b'A' ):
                        return_value = self.transmit_A(txt_inx, self.RxTmp)

                    if(chr.encode('ascii') == b'D' ):
                        return_value = self.transmit_D(txt_inx, self.RxTmp)

                    if(chr.encode('ascii') == b'L' ):
                        return_value = self.transmit_LU(txt_inx, self.RxTmp)

                    if(chr.encode('ascii') == b'U' ):
                        return_value = self.transmit_LU(txt_inx, self.RxTmp)

                    if(chr.encode('ascii')[:1] == b't' ):
                        return_value = self.transmit_t(txt_inx, self.RxTmp)

                    if(chr.encode('ascii')[:1] == b'T' ):
                        return_value = self.transmit_T(txt_inx, self.RxTmp)

                    if(chr.encode('ascii')[:1] == b'b' ):
                        return_value = self.transmit_b(txt_inx, self.RxTmp)




                return return_value

        else:
            # on startup, dialog aborted
            self.alive.clear()


    """  From Option Connect to USB ('s') ( Getting System )"""
    def transmit_s(self, inx, txt):

        val = {}

        val[0], txt, inx = self.convText(txt, inx)

        val[1], txt, inx = self.convText(txt, inx)

        lab_str, txt, inx  = self.convText(txt, inx)
        val[2] = lab_str[:1] + '.' + lab_str[1:]

        txt = txt[inx + 2:]
        s = int(len(txt)/2)

        if(s > 0x0F):
            txt = txt[2:]
        else:
            txt = txt[1:]

        txt_chr = ''

        for i in range(0, len(txt), 2):
            txt_chr += chr(int(txt[i:i+2], 16))

        val[3] = txt_chr

        return val

    """  From Option System to USB ('l') ( Tasks list ) """
    def transmit_l(self, inx, txt):

        val = {}

        for i in range(0, len(txt), 1):
            val[i], txt, inx = self.convText(txt, inx)

            if(len(txt) == 0):
                val.pop(i)
                break

        return val


    """  From Option Connect to USB ('t') ( Getting Task )"""
    def transmit_t(self, inx, txt):

        val = {}

        txt = txt[inx + 2:]
        inx = txt.find('7C')

        txt_tmp = txt[:inx]
        txt = txt[inx+2:]

        s = int((len(txt_tmp) -1)/2)

        if(s > 0x0F):
            txt_tmp = txt_tmp[2:]
        else:
            txt_tmp = txt_tmp[1:]

        txt_chr = ''

        for i in range(0, len(txt_tmp), 2):
            txt_chr += chr(int(txt_tmp[i:i+2], 16))

        val[0] = txt_chr

        inx = txt.find('7C')
        val[1] = str(int(txt[inx-1], 16))

        txt = txt[inx + 2:]
        inx = txt.find('7C')
        val[2] = txt[inx-1]

        val[3], txt, inx = self.convHex(txt, inx)
        val[4], txt, inx = self.convHex(txt, inx)
        val[5], txt, inx = self.convHex(txt, inx)
        val[6], txt, inx = self.convHex(txt, inx)

        return val

    """  From Option Connect to USB ('T') ( Getting Task Stack Address )"""
    def transmit_T(self, inx, txt):

        val = {}

        val[0], txt, inx = self.convHex(txt, inx)
        val[1], txt, inx = self.convHex(txt, inx)
        val[2], txt, inx = self.convHex(txt, inx)
        val[3], txt, inx = self.convHex(txt, inx)

        return val

    """  From Option Connect to USB ('b') ( Getting Task Stack Data )"""
    def transmit_b(self, inx, txt):

        return self.transmit_bfac(inx, txt)

    """  From Option System to USB ('f') ( FHT80 Default list ) """
    def transmit_f(self, inx, txt):

        return self.transmit_bfac(inx, txt)

    """  From Option System to USB ('a') ( TF Default list ) """
    def transmit_a(self, inx, txt):

        return self.transmit_bfac(inx, txt)

    """  From Option System to USB ('c') ( FHT-TF Paar Default list ) """
    def transmit_c(self, inx, txt):

        return self.transmit_bfac(inx, txt)

    """  From Option System to USB ('H') ( FHT80 Real Time list ) """
    def transmit_H(self, inx, txt):

        return self.transmit_bfac(inx, txt)

    """  From Option System to USB ('E') ( FHT80 Extensions Real Time list ) """
    def transmit_E(self, inx, txt):

        return self.transmit_bfac(inx, txt)

    """  From Option System to USB ('A') ( FHT80-TF Real Time list ) """
    def transmit_A(self, inx, txt):

        return self.transmit_bfac(inx, txt)

    """  From Option System to USB ('D') ( FHT80-TF Real Time list Clear) """
    def transmit_D(self, inx, txt):

        return self.transmit_bfac(inx, txt)

    """  From Option System to USB ('L') ( FHT80-TF Real Time Messages) """
    """  From Option System to USB ('U') ( TF UnIdentification  Real Time Messages) """
    def transmit_LU(self, inx, txt):

        txt_chr0 = ''
        txt_chr1 = ''
        txt_chr2 = ''
        txt_chr3 = ''

        txt = txt[inx + 2:]

        inx = txt.find('20')
        txt = txt[inx + 2:]

        txt_chr0, inx = self.convChrL(txt)
        txt_chr0 += ' '
        txt_chr0 = '   ' + txt_chr0
        txt = txt[inx + 2:]

        txt_chr1, inx = self.convChrL(txt)
        txt = txt[inx + 2:]

        if txt.find('20') != -1:
            txt_chr2, inx = self.convChrL(txt)
            txt_chr1 += ' '
            txt_chr2 += ' '
            txt = txt[inx + 2:]
        else:
            txt_chr1 = hex(int(txt_chr1)).upper()[2:] + ' '

        inx = txt.find('DA')
        txt = txt[:inx]

        for i in range(0, len(txt), 2):
            txt_chr3 += chr(int(txt[i:i+2], 16))

        txt_chr3 = hex(int(txt_chr3)).upper()[2:]
        if len(txt_chr3) < 2:
            txt_chr3 = '0' + txt_chr3

        return txt_chr0 + txt_chr1 + txt_chr2 + txt_chr3

########################################################################################################################
    def convText(self, txt, inx):

        txt = txt[inx + 2:]
        inx = txt.find('7C')

        if(inx == -1):
            return '', '', 0

        return str(int(txt[:inx], 16)), txt, inx

    def convHex(self, txt, inx):

        txt = txt[inx + 2:]
        inx = txt.find('7C')

        if (inx < 1) & (inx != -1):
            inx += 2

        return 'x' + txt[:inx], txt, inx

    def convChr(self, txt):

        txt_inx = txt.find('7C')
        txt_chr = txt[:txt_inx]

        return base64.b16decode(txt_chr), txt_inx

    def convChrL(self, txt):
        txt_chr = ''

        inx = txt.find('20')

        for i in range(0, len(txt), 2):
            if chr(int(txt[i:i+2], 16)) != ' ':
                txt_chr += chr(int(txt[i:i+2], 16))
            else:
                break

        return txt_chr, inx

    def transmit_bfac(self, inx, txt):

        val = {}

        for i in range(0, len(txt), 1):
            val[i], txt, inx = self.convHex(txt, inx)

            if(len(txt) == 0):
                val.pop(i)
                break

        return val