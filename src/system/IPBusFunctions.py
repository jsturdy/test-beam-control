import sys, os, time, signal, random

# Get IPBus
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ipbus")
from PyChipsUser import *

#
class GLIB:

    ipbus = False
    window = False

    #####################################
    #   Open the connection             #
    #####################################

    # Create IPBus
    def __init__(self):
        f = open(os.path.dirname(os.path.abspath(__file__)) + "/glib_ip.dat", "r")
        ipaddress = f.readline().strip()
        f.close()
        ipbusAddrTable = AddressTable(os.path.dirname(os.path.abspath(__file__)) + "/register_mapping.dat")
        self.ipbus = ChipsBusUdp(ipbusAddrTable, ipaddress, 50001)

    #####################################
    #   Add graphic support             #
    #####################################

    # Set window
    def setWindow(self, window):
        self.window = window

    #####################################
    #   Add error support               #
    #####################################

    # Print error
    def throwError(self, error, ignoreError = False):
        if (self.window != False and ignoreError == False):
            self.window.throwError(error)

    #####################################
    #   Getter and setter               #
    #####################################

    # Read operation
    def get(self, register, ignoreError = False):
        for i in range(0, 5):
            try:
                controlChar = self.ipbus.read(register)
                return controlChar
            except ChipsException, e:
                pass
        self.throwError("Could not read " + register, ignoreError)
        return False

    # Write operation
    def set(self, register, value, ignoreError = False):
        for i in range(0, 5):
            try:
                self.ipbus.write(register, value)
                return True
            except ChipsException, e:
                pass
        self.throwError("Could not write " + register, ignoreError)
        return False

    #####################################
    #   VFAT2 helper functions          #
    #####################################

    # Read VFAT2 register
    def getVFAT2(self, num, register, ignoreError = False):
        value = self.get("vfat2_" + str(num) + "_" + register, ignoreError)
        if (value == False):
            return False
        elif (((value & 0x4000000) >> 26) == 1):
            self.throwError("VFAT2 not found!", ignoreError)
            return False
        else:
            return (value & 0xff)

    # Write VFAT2 register
    def setVFAT2(self, num, register, value, ignoreError = False):
        return self.set("vfat2_" + str(num) + "_" + register, value, ignoreError)

    # Test if VFAT2 is connected
    def isVFAT2(self, num):
        # Test read
        chipId = self.get("vfat2_" + str(num) + "_chipid0", True)
        #
        if (chipId == False):
            return False
        elif (((chipId & 0x4000000) >> 26) == 1):
            return False
        else:
            return True

    # Save VFAT2 configuration
    def saveVFAT2(self, num):
        if (self.isVFAT2(num) == False):
            return []
        else:
            data = dict()
            data["ctrl0"] = self.getVFAT2(num, "ctrl0")
            data["ctrl1"] = self.getVFAT2(num, "ctrl1")
            data["ctrl2"] = self.getVFAT2(num, "ctrl2")
            data["ctrl3"] = self.getVFAT2(num, "ctrl3")
            data["ipreampin"] = self.getVFAT2(num, "ipreampin")
            data["ipreampfeed"] = self.getVFAT2(num, "ipreampfeed")
            data["ipreampout"] = self.getVFAT2(num, "ipreampout")
            data["ishaper"] = self.getVFAT2(num, "ishaper")
            data["ishaperfeed"] = self.getVFAT2(num, "ishaperfeed")
            data["icomp"] = self.getVFAT2(num, "icomp")
            data["chipid0"] = self.getVFAT2(num, "chipid0")
            data["chipid1"] = self.getVFAT2(num, "chipid1")
            data["upsetreg"] = self.getVFAT2(num, "upsetreg")
            data["hitcount0"] = self.getVFAT2(num, "hitcount0")
            data["hitcount1"] = self.getVFAT2(num, "hitcount1")
            data["hitcount2"] = self.getVFAT2(num, "hitcount2")
            data["latency"] = self.getVFAT2(num, "latency")
            data["vcal"] = self.getVFAT2(num, "vcal")
            data["vthreshold1"] = self.getVFAT2(num, "vthreshold1")
            data["vthreshold2"] = self.getVFAT2(num, "vthreshold2")
            data["calphase"] = self.getVFAT2(num, "calphase")
            for i in range(1, 129):
                data["channel"+str(i)] = self.getVFAT2(num, "channel"+str(i))
            return data

    # Restore VFAT2 configuration
    def restoreVFAT2(self, num, saved):
        if (self.isVFAT2(num) == False):
            return False
        else:
            self.setVFAT2(num, "ctrl0", data["ctrl0"])
            self.setVFAT2(num, "ctrl1", data["ctrl1"])
            self.setVFAT2(num, "ctrl2", data["ctrl2"])
            self.setVFAT2(num, "ctrl3", data["ctrl3"])
            self.setVFAT2(num, "ipreampin", data["ipreampin"])
            self.setVFAT2(num, "ipreampfeed", data["ipreampfeed"])
            self.setVFAT2(num, "ipreampout", data["ipreampout"])
            self.setVFAT2(num, "ishaper", data["ishaper"])
            self.setVFAT2(num, "ishaperfeed", data["ishaperfeed"])
            self.setVFAT2(num, "icomp", data["icomp"])
            self.setVFAT2(num, "latency", data["latency"])
            self.setVFAT2(num, "vcal", data["vcal"])
            self.setVFAT2(num, "vthreshold1", data["vthreshold1"])
            self.setVFAT2(num, "vthreshold2", data["vthreshold2"])
            self.setVFAT2(num, "calphase", data["calphase"])
            for i in range(1, 129):
                self.setVFAT2(num, "channel"+str(i), data["channel"+str(i)])
            self.set("oh_resync", 0x1)
            return True


