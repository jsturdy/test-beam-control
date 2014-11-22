import sys, os, time, signal, random

# Get IPBus
ipbus_path = os.path.dirname(os.path.abspath(__file__)) + "/ipbus"
sys.path.append(ipbus_path)
from PyChipsUser import *

#
class GLIB:

    ipbus = False
    window = False

    # Create IPBus
    def __init__(self):
        f = open(os.path.dirname(os.path.abspath(__file__)) + "/glib_ip.dat", "r")
        ipaddress = f.readline().strip()
        f.close()
        ipbusAddrTable = AddressTable(os.path.dirname(os.path.abspath(__file__)) + "/register_mapping.dat")
        self.ipbus = ChipsBusUdp(ipbusAddrTable, ipaddress, 50001)

    # Set window
    def setWindow(self, window):
        self.window = window

    # Read operation
    def get(self, register):
        for i in range(0, 5):
            try:
                controlChar = self.ipbus.read(register)
                return controlChar
            except ChipsException, e:
                pass
        self.printError("Could not read " + register)
        return False

    # Write operation
    def set(self, register, value):
        for i in range(0, 5):
            try:
                self.ipbus.write(register, value)
                return True
            except ChipsException, e:
                pass
        self.printError("Could not write " + register)
        return False

    # Read VFAT2 register
    def getVFAT2(self, num, register):
        value = self.get("vfat2_" + str(num) + "_" + register)
        if (((value & 0x4000000) >> 26) == 1):
            return False
        else:
            return (value & 0xff)

    # Write VFAT2 register
    def setVFAT2(self, num, register, value):
        return self.set("vfat2_" + str(num) + "_" + register, value)

    # Test if VFAT2 is connected
    def isVFAT2(self, num):
        # Test read
        chipId = self.get("vfat2_" + str(num) + "_chipid0")
        #
        if (chipId == False):
            return False
        elif (((chipId & 0x4000000) >> 26) == 1):
            return False
        else:
            return True

    # Print error
    def printError(self, error):
        if (self.window != False):
            self.window.printError(error)
