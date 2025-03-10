import sys, os, time

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
        if (self.window != False and ignoreError == False): self.window.throwError(error)

    #####################################
    #   Getter and setter               #
    #####################################

    # Read operation
    def get(self, register, ignoreError = False):
        for i in range(0, 2):
            try:
                controlChar = self.ipbus.read(register)
                return controlChar
            except ChipsException, e:
                time.sleep(0.1)
                pass
        self.throwError("Could not read " + register, ignoreError)
        return False

    # Write operation
    def set(self, register, value, ignoreError = False): 
        for i in range(0, 2):
            try:
                self.ipbus.write(register, value)
                return True
            except ChipsException, e:
                time.sleep(0.1)
                pass
        self.throwError("Could not write " + register, ignoreError)
        return False

    #####################################
    #   VFAT2 helper functions          #
    #####################################

    # Read VFAT2 register
    def getVFAT2(self, num, register, ignoreError = False):
        value = self.get("vfat2_" + str(num) + "_" + register, ignoreError)
        if (value == False): return False
        elif (((value & 0x4000000) >> 26) == 1):
            self.throwError("VFAT2 not found!", ignoreError)
            return False
        else: return (value & 0xff)

    # Write VFAT2 register
    def setVFAT2(self, num, register, value, ignoreError = False):
        return self.set("vfat2_" + str(num) + "_" + register, value, ignoreError)

    # Test if VFAT2 is connected
    def isVFAT2Present(self, num):
        # Test read
        chipId = self.get("vfat2_" + str(num) + "_chipid0", True)
        #
        if (chipId == False): return False
        elif (((chipId & 0x4000000) >> 26) == 1): return False
        else: return True

    # Test if VFAT2 is connected
    def isVFAT2Running(self, num):
        # Test read
        ctrl0 = self.get("vfat2_" + str(num) + "_ctrl0", True)
        #
        if (ctrl0 == False): return False
        elif (((ctrl0 & 0x4000000) >> 26) == 1): return False
        elif ((ctrl0 & 0x1) == 0x1): return True
        else: return False

    # Save VFAT2 configuration
    def saveVFAT2(self, num):
        if (self.isVFAT2Present(num) == False): return dict()
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
            return data

    # Restore VFAT2 configuration
    def restoreVFAT2(self, num, data):
        if (self.isVFAT2Present(num) == False): return False
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
            self.set("oh_resync", 0x1)
            return True

    # Save system configuration
    def saveSystem(self):
        data = dict()
        data["oh_trigger_source"] = self.get("oh_trigger_source")
        data["oh_sbit_select"] = self.get("oh_sbit_select")
        data["glib_sbit_select"] = self.get("glib_sbit_select")
        data["oh_vfat2_src_select"] = self.get("oh_vfat2_src_select")
        data["oh_cdce_src_select"] = self.get("oh_cdce_src_select")
        data["oh_vfat2_fallback"] = self.get("oh_vfat2_fallback")
        data["oh_cdce_fallback"] = self.get("oh_cdce_fallback")
        return data

    # Restore system configuration
    def restoreSystem(self):
        self.set("oh_trigger_source", data["oh_trigger_source"])
        self.set("oh_sbit_select", data["oh_sbit_select"])
        self.set("glib_sbit_select", data["glib_sbit_select"])
        self.set("oh_vfat2_src_select", data["oh_vfat2_src_select"])
        self.set("oh_cdce_src_select", data["oh_cdce_src_select"])
        self.set("oh_vfat2_fallback", data["oh_vfat2_fallback"])
        self.set("oh_cdce_fallback", data["oh_cdce_fallback"])

    # Get the counters
    def saveCounters(self):
        data = dict()
        data["glib_error_counter"] = self.get("glib_error_counter")
        data["glib_vfat2_rx_counter"] = self.get("glib_vfat2_rx_counter")
        data["glib_vfat2_tx_counter"] = self.get("glib_vfat2_tx_counter")
        data["glib_reg_rx_counter"] = self.get("glib_reg_rx_counter")
        data["glib_reg_tx_counter"] = self.get("glib_reg_tx_counter")
        data["oh_error_counter"] = self.get("oh_error_counter")
        data["oh_vfat2_rx_counter"] = self.get("oh_vfat2_rx_counter")
        data["oh_vfat2_tx_counter"] = self.get("oh_vfat2_tx_counter")
        data["oh_reg_rx_counter"] = self.get("oh_reg_rx_counter")
        data["oh_reg_tx_counter"] = self.get("oh_reg_tx_counter")
        data["oh_ext_lv1a_counter"] = self.get("oh_ext_lv1a_counter")
        data["oh_int_lv1a_counter"] = self.get("oh_int_lv1a_counter")
        data["oh_del_lv1a_counter"] = self.get("oh_del_lv1a_counter")
        data["oh_lv1a_counter"] = self.get("oh_lv1a_counter")
        data["oh_int_calpulse_counter"] = self.get("oh_int_calpulse_counter")
        data["oh_del_calpulse_counter"] = self.get("oh_del_calpulse_counter")
        data["oh_calpulse_counter"] = self.get("oh_calpulse_counter")
        data["oh_resync_counter"] = self.get("oh_resync_counter")
        data["oh_bc0_counter"] = self.get("oh_bc0_counter")
        return data

    # Reset the counters
    def resetCounters(self):
        self.set('glib_reset_error_counter', 0)
        self.set('glib_reset_vfat2_rx_counter', 0)
        self.set('glib_reset_vfat2_tx_counter', 0)
        self.set('glib_reset_reg_rx_counter', 0)
        self.set('glib_reset_reg_tx_counter', 0)
        self.set('oh_reset_error_counter', 0)
        self.set('oh_reset_vfat2_rx_counter', 0)
        self.set('oh_reset_vfat2_tx_counter', 0)
        self.set('oh_reset_reg_rx_counter', 0)
        self.set('oh_reset_reg_tx_counter', 0)
        self.set('oh_reset_ext_lv1a_counter', 0)
        self.set('oh_reset_int_lv1a_counter', 0)
        self.set('oh_reset_del_lv1a_counter', 0)
        self.set('oh_reset_lv1a_counter', 0)
        self.set('oh_reset_int_calpulse_counter', 0)
        self.set('oh_reset_del_calpulse_counter', 0)
        self.set('oh_reset_calpulse_counter', 0)
        self.set('oh_reset_resync_counter', 0)
        self.set('oh_reset_bc0_counter', 0)
