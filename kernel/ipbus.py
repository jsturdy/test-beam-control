import sys, os, time

# Get IPBus
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ipbus")
import uhal

#
class GLIB:

    slot   = -1
    glib   = False
    window = False
    glib_base = "GLIB.GLIB"
    oh_base   = "OptoHybrid.OptoHybrid"
    vfat_base = "OptoHybrid.OptoHybrid.GEB.VFATS"

    links = False
    oh_control_link   = 0
    glib_control_link = 0 
    #####################################
    #   Open the connection             #
    #####################################

    # Create uHAL device
    def __init__(self, slot, links):
        self.slot = 160+slot
        self.links = links
        self.oh_control_link   = links[links.keys()[0]]
        self.glib_control_link = links.keys()[0]
        ipaddr = '192.168.0.%d'%(self.slot)
        #address_table = "file://${BUILD_HOME}/data/testbeam_registers.xml"
        address_table = "file://${BUILD_HOME}/data/full_system_address_table.xml"
        #address_table = "file://${BUILD_HOME}/data/glib_address_table.xml"
        #address_table = "file://${BUILD_HOME}/data/optohybrid_address_table.xml"
        #address_table = "file://${BUILD_HOME}/data/geb_vfat_address_table.xml"
        uri = "chtcp-2.0://localhost:10203?target=%s:50001"%(ipaddr)
        self.glib = uhal.getDevice( "glib" , uri, address_table )
        #self.glib_base = self.glib.getNode("GLIB.GLIB")
        #self.oh_base   = self.glib.getNode("OptoHybrid.OptoHybrid")
        #self.vfat_base = self.glib.getNode("OptoHybrid.OptoHybrid.GEB.VFATS")
        self.printInfo(self.vfat_base)
        self.printInfo(self.glib_base)
        self.printInfo(self.oh_base)
        self.printInfo("OptoHybrid.OptoHybrid.OptoHybrid_LINKS.LINK1.CLOCKING.VFAT.SOURCE" in self.glib.getNodes())
        #print self.glib_base.getNodes()
        #print "GLIB.GLIB_LINKS.LINK1.OPTICAL_LINKS.Counter.SntRegRequests" in self.glib_base.getNodes()
        #exit(1)
    #####################################
    #   Add graphic support             #
    #####################################

    # Set window
    def setWindow(self, window):
        self.window = window

    #####################################
    #   Add error support               #
    #####################################

    # Print info
    def printInfo(self, info, ignoreError = False):
        if (self.window != False and ignoreError == False): self.window.printInfo(info)

    # Print error
    def throwError(self, error, ignoreError = False):
        if (self.window != False and ignoreError == False): self.window.throwError(error)

    #####################################
    #   Getter and setter               #
    #####################################

    # Read operation
    def get(self, register, ignoreError = False):
        if not self.glib.getNode(register):
            self.throwError("Could not find %s in address table"%(register), ignoreError)
            return False
        address = self.glib.getNode(register).getAddress()
        for i in range(0, 5):
            #self.printInfo("read trial %d on register %s (0x%x)"%(i,register,address))
            try:
                controlChar = self.glib.getNode(register).read()
                self.glib.dispatch()
                return controlChar
            except uhal.exception, e:
                #self.printInfo(e.str())
                time.sleep(0.01)
                pass
        self.throwError("Could not read " + register, ignoreError)
        return False

    # Write operation
    def set(self, register, value, ignoreError = False): 
        if not self.glib.getNode(register):
            self.throwError("Could not find %s in address table"%(register), ignoreError)
            return False
        for i in range(0, 5):
            try:
                self.glib.getNode(register).write(value)
                self.glib.dispatch()
                return True
            except uhal.exception, e:
                time.sleep(0.01)
                pass
        self.throwError("Could not write " + register, ignoreError)
        return False

    #####################################
    #   GLIB helper functions           #
    #####################################

    # Read GLIB register
    def getGLIB(self, register, ignoreError = False):
        value = self.get("%s.%s"%(self.glib_base,register), ignoreError)
        if (value == False): return False
        elif (((value & 0x4000000) >> 26) == 1):
            self.throwError("GLIB register %s not found!"%(register), ignoreError)
            return False
        else: return (value & 0xff)

    # Write GLIB register
    def setGLIB(self, register, value, ignoreError = False):
        return self.set("%s.%s"%(self.glib_base,register), value, ignoreError)

    # Flush the tracking data FIFO
    def flushFIFO(self, ignoreError = False):
        register = "GLIB_LINKS.LINK%d.TRK_FIFO.FLUSH"%(self.glib_control_link)
        value = 0x1
        return self.set("%s.%s"%(self.glib_base,register), value, ignoreError)

    # Query the tracking data FIFO depth
    def hasData(self, ignoreError = False):
        register = "OptoHybrid.OptoHybrid.GEB.TRK_DATA.COL%d.DATA_RDY"%(self.oh_control_link)
        value = 0x1
        return self.get("%s"%(register), ignoreError)

    #####################################
    #   OH helper functions             #
    #####################################

    # Read OH register
    def getOH(self, register, ignoreError = False):
        value = self.get("%s.%s"%(self.oh_base,register), ignoreError)
        if (value == False): return False
        elif (((value & 0x4000000) >> 26) == 1):
            self.throwError("OH register %s not found!"%(register), ignoreError)
            return False
        else: return (value & 0xff)

    # Write OH register
    def setOH(self, register, value, ignoreError = False):
        return self.set("%s.%s"%(self.oh_base,register), value, ignoreError)

    # Send an L1A
    def sendL1A(self, ignoreError = False):
        register = "OptoHybrid_LINKS.LINK%d.FAST_COM.Send.L1A"%(self.oh_control_link)
        value = 0x1
        return self.set("%s.%s"%(self.oh_base,register), value, ignoreError)

    # Send an CalPulse
    def sendCalPulse(self, ignoreError = False):
        register = "OptoHybrid_LINKS.LINK%d.FAST_COM.Send.CalPulse"%(self.oh_control_link)
        value = 0x1
        return self.set("%s.%s"%(self.oh_base,register), value, ignoreError)

    # Send an Resync
    def sendResync(self, ignoreError = False):
        register = "OptoHybrid_LINKS.LINK%d.FAST_COM.Send.Resync"%(self.oh_control_link)
        value = 0x1
        return self.set("%s.%s"%(self.oh_base,register), value, ignoreError)

    # Send an BC0
    def sendBC0(self, ignoreError = False):
        register = "OptoHybrid_LINKS.LINK%d.FAST_COM.Send.BC0"%(self.oh_control_link)
        value = 0x1
        return self.set("%s.%s"%(self.oh_base,register), value, ignoreError)

    #####################################
    #   VFAT2 helper functions          #
    #####################################

    # Read VFAT2 register
    def getVFAT2(self, num, register, ignoreError = False):
        value = self.get("%s.VFAT%d.%s"%(self.vfat_base,num,register), ignoreError)
        if (value == False): return False
        elif (((value & 0x4000000) >> 26) == 1):
            self.throwError("VFAT2 register %s not found!"%(register), ignoreError)
            return False
        else: return (value & 0xff)

    # Write VFAT2 register
    def setVFAT2(self, num, register, value, ignoreError = False):
        return self.set("%s.VFAT%d.%s"%(self.vfat_base,num,register), value, ignoreError)

    # Get VFAT2 channel register
    def getVFAT2Channel(self, num, chan, ignoreError = False):
        return self.getVFAT2(num, "VFATChannels.ChanReg%d"%(chan), ignoreError)

    # Write VFAT2 channel register
    def setVFAT2Chanel(self, num, register, value, ignoreError = False):
        return self.setVFAT2(num, "VFATChannels.ChanReg%d"%(chan), value, ignoreError)

    # Enable run mode for VFAT2
    def enableVFAT2(self, num, ignoreError = False):
        cr0val = self.getVFAT2(num, "ContReg0", ignoreError)
        #self.printInfo("Enabling VFAT%d returns CR0 0x%08x"%(num,cr0val))
        cr0val |= 0x00000001
        #self.printInfo("Enabling VFAT%d returns CR0 0x%08x"%(num,cr0val))
        return self.setVFAT2(num, "ContReg0", cr0val, ignoreError)

    # Disable run mode for VFAT2
    def disableVFAT2(self, num, ignoreError = False):
        cr0val = self.getVFAT2(num, "ContReg0", ignoreError)
        #self.printInfo("Disabling VFAT%d returns CR0 0x%08x"%(num,cr0val))
        cr0val &= 0xFFFFFFFE
        #self.printInfo("Disabling VFAT%d setting CR0 0x%08x"%(num,cr0val))
        return self.setVFAT2(num, "ContReg0", cr0val, ignoreError)

    # Test if VFAT2 is connected
    def isVFAT2Present(self, num):
        # Test read
        chipId = self.get("%s.VFAT%d.ChipID0"%(self.vfat_base,num), True)
        #
        #self.printInfo("VFAT2 chip%d returns chipid0 0x%08x"%(num,chipId))
        if (chipId == False): return False
        elif (((chipId & 0x4000000) >> 26) == 1): return False
        else: return True

    # Test if VFAT2 is connected
    def isVFAT2Running(self, num):
        # Test read
        ctrl0 = self.get("%s.VFAT%d.ContReg0"%(self.vfat_base,num), True)
        #
        #self.printInfo("VFAT2 chip%d returns ctrl0 0x%08x"%(num,ctrl0))
        if (ctrl0 == False): return False
        elif (((ctrl0 & 0x4000000) >> 26) == 1): return False
        elif ((ctrl0 & 0x1) == 0x1): return True
        else: return False

    # Save VFAT2 configuration
    def saveVFAT2(self, num):
        if (self.isVFAT2Present(num) == False): return dict()
        else:
            data = dict()
            data["ctrl0"]       = self.getVFAT2(num, "ContReg0")
            data["ctrl1"]       = self.getVFAT2(num, "ContReg1")
            data["ctrl2"]       = self.getVFAT2(num, "ContReg2")
            data["ctrl3"]       = self.getVFAT2(num, "ContReg3")
            data["ipreampin"]   = self.getVFAT2(num, "IPreampIn")
            data["ipreampfeed"] = self.getVFAT2(num, "IPreampFeed")
            data["ipreampout"]  = self.getVFAT2(num, "IPreampOut")
            data["ishaper"]     = self.getVFAT2(num, "IShaper")
            data["ishaperfeed"] = self.getVFAT2(num, "IShaperFeed")
            data["icomp"]       = self.getVFAT2(num, "IComp")
            data["chipid0"]     = self.getVFAT2(num, "ChipID0")
            data["chipid1"]     = self.getVFAT2(num, "ChipID1")
            data["upsetreg"]    = self.getVFAT2(num, "UpsetReg")
            data["hitcount0"]   = self.getVFAT2(num, "HitCount0")
            data["hitcount1"]   = self.getVFAT2(num, "HitCount1")
            data["hitcount2"]   = self.getVFAT2(num, "HitCount2")
            data["latency"]     = self.getVFAT2(num, "Latency")
            data["vcal"]        = self.getVFAT2(num, "VCal")
            data["vthreshold1"] = self.getVFAT2(num, "VThreshold1")
            data["vthreshold2"] = self.getVFAT2(num, "VThreshold2")
            data["calphase"]    = self.getVFAT2(num, "CalPhase")
            return data

    # Restore VFAT2 configuration
    def restoreVFAT2(self, num, data):
        if (self.isVFAT2Present(num) == False): return False
        else:
            self.setVFAT2(num, "ContReg0",    data["ctrl0"])
            self.setVFAT2(num, "ContReg1",    data["ctrl1"])
            self.setVFAT2(num, "ContReg2",    data["ctrl2"])
            self.setVFAT2(num, "ContReg3",    data["ctrl3"])
            self.setVFAT2(num, "IPreampIn",   data["ipreampin"])
            self.setVFAT2(num, "IPreampFeed", data["ipreampfeed"])
            self.setVFAT2(num, "IPreampOut",  data["ipreampout"])
            self.setVFAT2(num, "IShaper",     data["ishaper"])
            self.setVFAT2(num, "IShaperFeed", data["ishaperfeed"])
            self.setVFAT2(num, "IComp",       data["icomp"])
            self.setVFAT2(num, "Latency",     data["latency"])
            self.setVFAT2(num, "VCal",        data["vcal"])
            self.setVFAT2(num, "VThreshold1", data["vthreshold1"])
            self.setVFAT2(num, "VThreshold2", data["vthreshold2"])
            self.setVFAT2(num, "CalPhase",    data["calphase"])
            self.sendResync()
            return True

    # Save system configuration
    def saveSystem(self):
        data = dict()
        data["oh_trigger_source"]   = self.getOH("OptoHybrid_LINKS.LINK%d.TRIGGER.SOURCE"%(self.oh_control_link))
        data["oh_sbit_select"]      = self.getOH("OptoHybrid_LINKS.LINK%d.TRIGGER.TDC_SBits"%(self.oh_control_link))
        data["oh_vfat2_src_select"] = self.getOH("OptoHybrid_LINKS.LINK%d.CLOCKING.VFAT.SOURCE"%(self.oh_control_link))
        data["oh_cdce_src_select"]  = self.getOH("OptoHybrid_LINKS.LINK%d.CLOCKING.CDCE.SOURCE"%(self.oh_control_link))
        data["oh_vfat2_fallback"]   = self.getOH("OptoHybrid_LINKS.LINK%d.CLOCKING.VFAT.FALLBACK"%(self.oh_control_link))
        data["oh_cdce_fallback"]    = self.getOH("OptoHybrid_LINKS.LINK%d.CLOCKING.CDCE.FALLBACK"%(self.oh_control_link))
        data["glib_sbit_select"]    = self.getGLIB("GLIB_LINKS.LINK%d.TRIGGER.TDC_SBits"%(self.glib_control_link))
        data["glib_trigger_source"] = self.getGLIB("GLIB_LINKS.LINK%d.TRIGGER.SOURCE"%(self.glib_control_link))
        return data

    # Restore system configuration
    def restoreSystem(self):
        self.setOH("OptoHybrid_LINKS.LINK%d.TRIGGER.SOURCE"%(self.oh_control_link),         data["oh_trigger_source"])
        self.setOH("OptoHybrid_LINKS.LINK%d.TRIGGER.TDC_SBits"%(self.oh_control_link),      data["oh_sbit_select"])
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.VFAT.SOURCE"%(self.oh_control_link),   data["oh_vfat2_src_select"])
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.CDCE.SOURCE"%(self.oh_control_link),   data["oh_cdce_src_select"])
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.VFAT.FALLBACK"%(self.oh_control_link), data["oh_vfat2_fallback"])
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.CDCE.FALLBACK"%(self.oh_control_link), data["oh_cdce_fallback"])
        self.setGLIB("GLIB_LINKS.LINK%d.TRIGGER.TDC_SBits"%(self.glib_control_link),        data["glib_sbit_select"])
        self.getGLIB("GLIB_LINKS.LINK%d.TRIGGER.SOURCE"%(self.glib_control_link),           data["glib_trigger_source"])

    # Restore system configuration
    def systemDefault(self):
        self.setGLIB("GLIB_LINKS.LINK%d.TRIGGER.TDC_SBits"%(self.glib_control_link),        0x0)
        self.setGLIB("GLIB_LINKS.LINK%d.TRIGGER.SOURCE"%(self.glib_control_link),           0x2)
        self.setOH("OptoHybrid_LINKS.LINK%d.TRIGGER.SOURCE"%(self.oh_control_link),         0x2)
        self.setOH("OptoHybrid_LINKS.LINK%d.TRIGGER.TDC_SBits"%(self.oh_control_link),      0x0)
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.VFAT.SOURCE"%(self.oh_control_link),   0x1)
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.CDCE.SOURCE"%(self.oh_control_link),   0x1)
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.VFAT.FALLBACK"%(self.oh_control_link), 0x0)
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.CDCE.FALLBACK"%(self.oh_control_link), 0x0)

    # Set the OH trigger source
    def setOHTriggerSource(self, source):
        self.setOH("OptoHybrid_LINKS.LINK%d.TRIGGER.SOURCE"%(self.oh_control_link), source)

    # Set the GLIB trigger source
    def setGLIBTriggerSource(self, source):
        self.setGLIB("GLIB_LINKS.LINK%d.TRIGGER.SOURCE"%(self.oh_control_link), source)

    # Set the SBit source
    def setSBitSource(self, source):
        self.setGLIB("GLIB_LINKS.LINK%d.TRIGGER.TDC_SBits"%(self.glib_control_link),   source)
        self.setOH("OptoHybrid_LINKS.LINK%d.TRIGGER.TDC_SBits"%(self.oh_control_link), source)

    # Set the VFAT clock source
    def setVFATClkSrc(self, source):
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.VFAT.SOURCE"%(self.oh_control_link), source)

    # Set the VFAT clock fallback
    def setVFATClkBkp(self, backup):
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.VFAT.FALLBACK"%(self.oh_control_link), backup)

    # Set the CDCE clock source
    def setCDCEClkSrc(self, source):
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.CDCE.SOURCE"%(self.oh_control_link), source)

    # Set the CDCE clock fallback
    def setCDCEClkBkp(self, backup):
        self.setOH("OptoHybrid_LINKS.LINK%d.CLOCKING.CDCE.FALLBACK"%(self.oh_control_link), backup)

    # Get the counters
    def saveCounters(self):
        data = dict()
        for link in self.links.keys():
            data["glib_link%d_error_counter"%(link)]             = self.getGLIB("GLIB_LINKS.LINK%d.OPTICAL_LINKS.Counter.LinkErr"%(link)   )
            data["glib_link%d_vfat2_rx_counter"%(link)]          = self.getGLIB("GLIB_LINKS.LINK%d.OPTICAL_LINKS.Counter.RecI2CRequests"%(link))
            data["glib_link%d_vfat2_tx_counter"%(link)]          = self.getGLIB("GLIB_LINKS.LINK%d.OPTICAL_LINKS.Counter.SntI2CRequests"%(link))
            data["glib_link%d_reg_rx_counter"%(link)]            = self.getGLIB("GLIB_LINKS.LINK%d.OPTICAL_LINKS.Counter.RecRegRequests"%(link)  )
            data["glib_link%d_reg_tx_counter"%(link)]            = self.getGLIB("GLIB_LINKS.LINK%d.OPTICAL_LINKS.Counter.SntRegRequests"%(link)  )

            data["oh_link%d_error_counter"%(self.links[link])]        = self.getOH("OptoHybrid_LINKS.LINK%d.OPTICAL_LINKS.Counter.LinkErr"%(self.links[link])       )
            data["oh_link%d_vfat2_rx_counter"%(self.links[link])]     = self.getOH("OptoHybrid_LINKS.LINK%d.OPTICAL_LINKS.Counter.RecI2CRequests"%(self.links[link])    )
            data["oh_link%d_vfat2_tx_counter"%(self.links[link])]     = self.getOH("OptoHybrid_LINKS.LINK%d.OPTICAL_LINKS.Counter.SntI2CRequests"%(self.links[link])    )
            data["oh_link%d_reg_rx_counter"%(self.links[link])]       = self.getOH("OptoHybrid_LINKS.LINK%d.OPTICAL_LINKS.Counter.RecRegRequests"%(self.links[link])      )
            data["oh_link%d_reg_tx_counter"%(self.links[link])]       = self.getOH("OptoHybrid_LINKS.LINK%d.OPTICAL_LINKS.Counter.SntRegRequests"%(self.links[link])      )

        data["oh_ext_lv1a_counter"]     = self.getOH("OptoHybrid_LINKS.LINK%d.COUNTERS.L1A.External"%(self.oh_control_link)    )
        data["oh_int_lv1a_counter"]     = self.getOH("OptoHybrid_LINKS.LINK%d.COUNTERS.L1A.Internal"%(self.oh_control_link)    )
        data["oh_del_lv1a_counter"]     = self.getOH("OptoHybrid_LINKS.LINK%d.COUNTERS.L1A.Delayed"%( self.oh_control_link)    )
        data["oh_lv1a_counter"]         = self.getOH("OptoHybrid_LINKS.LINK%d.COUNTERS.L1A.Total"%(   self.oh_control_link)    )
        data["oh_int_calpulse_counter"] = self.getOH("OptoHybrid_LINKS.LINK%d.COUNTERS.CalPulse.Internal"%(self.oh_control_link))
        data["oh_del_calpulse_counter"] = self.getOH("OptoHybrid_LINKS.LINK%d.COUNTERS.CalPulse.Delayed"%( self.oh_control_link))
        data["oh_calpulse_counter"]     = self.getOH("OptoHybrid_LINKS.LINK%d.COUNTERS.CalPulse.Total"%(   self.oh_control_link))
        data["oh_resync_counter"]       = self.getOH("OptoHybrid_LINKS.LINK%d.COUNTERS.Resync"%( self.oh_control_link)      )
        data["oh_bc0_counter"]          = self.getOH("OptoHybrid_LINKS.LINK%d.COUNTERS.BC0"%(    self.oh_control_link)      )
        data["oh_bx_counter"]           = self.getOH("OptoHybrid_LINKS.LINK%d.COUNTERS.BXCount"%(self.oh_control_link)      )
        return data

    # Reset the counters
    def resetCounters(self):
        for link in self.links.keys():
            self.setGLIB("GLIB_LINKS.LINK%d.OPTICAL_LINKS.Resets.LinkErr"%(       link),0x0)
            self.setGLIB("GLIB_LINKS.LINK%d.OPTICAL_LINKS.Resets.RecI2CRequests"%(link),0x0)
            self.setGLIB("GLIB_LINKS.LINK%d.OPTICAL_LINKS.Resets.SntI2CRequests"%(link),0x0)
            self.setGLIB("GLIB_LINKS.LINK%d.OPTICAL_LINKS.Resets.RecRegRequests"%(link),0x0)
            self.setGLIB("GLIB_LINKS.LINK%d.OPTICAL_LINKS.Resets.SntRegRequests"%(link),0x0)
            
            self.setOH("OptoHybrid_LINKS.LINK%d.OPTICAL_LINKS.Resets.LinkErr"%(       self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.OPTICAL_LINKS.Resets.RecI2CRequests"%(self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.OPTICAL_LINKS.Resets.SntI2CRequests"%(self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.OPTICAL_LINKS.Resets.RecRegRequests"%(self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.OPTICAL_LINKS.Resets.SntRegRequests"%(self.links[link]),0x0)
            
            self.setOH("OptoHybrid_LINKS.LINK%d.COUNTERS.RESETS.L1A.External"%(self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.COUNTERS.RESETS.L1A.Internal"%(self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.COUNTERS.RESETS.L1A.Delayed"%( self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.COUNTERS.RESETS.L1A.Total"%(   self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.COUNTERS.RESETS.CalPulse.Internal"%(self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.COUNTERS.RESETS.CalPulse.Delayed"%( self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.COUNTERS.RESETS.CalPulse.Total"%(   self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.COUNTERS.RESETS.Resync"%(self.links[link]),0x0)
            self.setOH("OptoHybrid_LINKS.LINK%d.COUNTERS.RESETS.BC0"%(   self.links[link]),0x0)
  
