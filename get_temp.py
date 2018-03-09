__author__ = 'Puleo'

import os
import glob
import time

class DS1820(object):
    """
	 much of this code is lifted from Adafruit web site
	 This class can be used to access one or more DS18B20 temperature sensors
	 It uses OS supplied drivers and one wire support must be enabled
	 To do this add the line
	 dtoverlay=w1-gpio,gpiopin=4,pullup=on
	 to the end of /boot/config.txt

	 The DS18B20 has three pins, looking at the flat side with the pins pointing
	 down pin 1 is on the left
	 connect pin 1 to GPIO ground
	 connect pin 2 to GPIO 4 *and* GPIO 3.3V via a 4k8 (4800 ohm) pullup resistor
	 connect pin 3 to GPIO 3.3V
	 You can connect more than one sensor to the same set of pins
	 Only one pullup resistor is required
    """

    def __init__(self):
        # load required kernel modules
        os.system('sudo modprobe w1-gpio pullup=1')
        os.system('sudo modprobe w1-therm strong_pullup=1')

        # Find file names for the sensor(s)
		# Sensors of the type DS1820 and DS18S20 have the Family Code 10, DS18B20 has Code 28 and DS1822 the 22

        device_folder = glob.glob('/sys/bus/w1/devices/' + '10*')
        self._num_devices = len(device_folder)
        self._device_file = list()
        i=0
        while i < self._num_devices:
            self._device_file.append(device_folder[i] + '/w1_slave')
            i += 1

    def _read_temp(self, index):
        # Issue one read to one sensor
		# you should not call this directly
        #f = open(self, self._device_file[index], 'r')
        f = open(self._device_file[index], 'r')
        lines = f.readlines()
        f.close()
        return lines

    def tempC(self,index = 0):
        # call this to get the temperature in degrees C
		# detected by a sensor
        lines = self._read_temp(index)
        retries = 5
        while (lines[0].strip()[-3:] != 'YES') and (retries > 0):
            # read failed so try again
            time.sleep(0.1)
            #print('Read Failed', retries)
            lines = self._read_temp(index)
            retries -= 1

        if retries == 0:
            return 998

        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp = lines[1][equals_pos + 2:]
            return float(temp)/1000
        else:
            # error
            return 999

    def tempAddr(self, index=0):
        line = self._device_file[index]
        line = line.replace('/sys/bus/w1/devices/', '')
        line = line.replace('/w1_slave', '')
        return line


    def device_count(self):
        # call this to see how many sensors have been detected
        return self._num_devices


    def loadDataTemp(self):
        addr = {}
        data = {}

        #x = get_temp.DS1820()
        count= self.device_count()
        row = 0
        while row < count:
            data[row] = self.tempC(row)
            addr[row] = self.tempAddr(row)
            row += 1

        return data, addr, count
