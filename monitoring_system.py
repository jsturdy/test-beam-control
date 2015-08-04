#!/bin/env python

# System imports
import time
from kernel import *

import uhal

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s", "--slot", type="int", dest="slot",
		  help="slot in uTCA crate", metavar="slot", default=4)

parser.add_option("-o", "--links", type="string", dest="activeLinks", action='append',
		  help="pair of connected optical links (GLIB,OH)", metavar="activeLinks", default=[])
(options, args) = parser.parse_args()

links = {}
for link in options.activeLinks:
	pair = map(int, link.split(","))
	links[pair[0]] = pair[1]
print "links", links

uhal.setLogLevelTo( uhal.LogLevel.FATAL )

if not links.keys():
    print "No optical links specified, exiting"
    exit(1)

# Create window
window = Window("System monitoring")

# Get GLIB access
glib = GLIB(options.slot,links)
glib.setWindow(window)

#########################################
#   Introduction Window                 #
#########################################

def introWindow():
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Instructions", "Subtitle")
    window.printLine(3, "This program allows you to control and monitor the system.")
    window.printLine(4, "Once the system is connected, it will show you the value written in the")
    window.printLine(5, "various registers and counters, and update them every few seconds.")
    window.printLine(7, "The list of actions that can be performed are listed on the bottom")
    window.printLine(8, "of the screen. Once connected, here are the possible actions:")
    window.printLine(9, "Press [r] to reset the counters.")
    window.printLine(10, "Press [s] to change the value of the registers.")
    window.printLine(11, "Press [d] to set the registers to their default value.")
    window.printLine(12, "Press [q] to quit the program.")
    window.printLine(13, "As you can see, when a key performs an action, it is placed between brackets.")
    window.printLine(15, "You can always exit the program by pressing [Ctrl+C].")
    window.printLine(-2, "Hint: here is what to do next (possible actions are always shown here)")
    window.printLine(-1, "Press [c] to continue.", "Options")
    window.waitForKey("c")

#########################################
#   Main window: view registers         #
#########################################

def mainWindow():
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Monitoring the system", "Subtitle")
    window.printLine(3, "Current value of the registers and counters: values that appear in red", "Highlight")
    window.printLine(4, "differ from the recommended value for data tacking (in parentheses).", "Highlight")
    window.printLine(-1, "Actions: [q]uit, [s]et the registers, [r]eset the counters, [d]efault values", "Options")
    # Go to non-blocking mode
    window.disableBlocking()
    # Stay in this window until command select
    while (True):
        # Get all the values to show
        system = glib.saveSystem()
        counters = glib.saveCounters()
        # Clear line
        window.clear(5, 1)
        #
        window.printLabel(0,  6,  24, "SBit VFAT2 select:",   (system["oh_sbit_select"] + 8))
        window.printLabel(0,  7,  24, "OH Trg src (1/2):",   system["oh_trigger_source"],   ("Error" if (system["oh_trigger_source"]   != 1 and system["oh_trigger_source"]   != 2) else "Success"))
        window.printLabel(0,  8,  24, "GLIB Trg src (1/2):", system["glib_trigger_source"], ("Error" if (system["glib_trigger_source"] != 1 and system["glib_trigger_source"] != 2) else "Success"))
        window.printLabel(27, 6,  24, "VFAT2 Clock (1):",    system["oh_vfat2_src_select"], ("Error" if (system["oh_vfat2_src_select"] != 1) else "Success"))
        window.printLabel(27, 7,  24, "CDCE Clock (1):",     system["oh_cdce_src_select"],  ("Error" if (system["oh_cdce_src_select"]  != 1) else "Success"))
        window.printLabel(54, 6,  24, "VFAT2 fallback (0):", system["oh_vfat2_fallback"],   ("Error" if (system["oh_vfat2_fallback"]   != 0) else "Success"))
        window.printLabel(54, 7,  24, "CDCE fallback (0):",  system["oh_cdce_fallback"],    ("Error" if (system["oh_cdce_fallback"]    != 0) else "Success"))
        window.printLabel(0,  9,  24, "Ext. LV1As:",     counters["oh_ext_lv1a_counter"])
        window.printLabel(0,  10, 24, "Int. LV1As:",     counters["oh_int_lv1a_counter"])
        window.printLabel(0,  11, 24, "Del. LV1As:",     counters["oh_del_lv1a_counter"])
        window.printLabel(0,  12, 24, "# LV1As:",        counters["oh_lv1a_counter"])
        window.printLabel(27, 9,  24, "Int. Calpulses:", counters["oh_int_calpulse_counter"])
        window.printLabel(27, 10, 24, "Del. Calpulses:", counters["oh_del_calpulse_counter"])
        window.printLabel(27, 11, 24, "# Calpulses:",    counters["oh_calpulse_counter"])
        window.printLabel(54, 9,  24, "# Resyncs:",      counters["oh_resync_counter"])
        window.printLabel(54, 10, 24, "# BC0s:",         counters["oh_bc0_counter"])
        for i,link in enumerate(links.keys()):
            window.printLabel(0,  14+(i*5), 24, "GLIB link%d errors:"%(link),    counters["glib_link%d_error_counter"%(link)])
            window.printLabel(0,  15+(i*5), 24, "GLIB link%d VFAT2 RX:"%(link),  counters["glib_link%d_vfat2_rx_counter"%(link)])
            window.printLabel(0,  16+(i*5), 24, "GLIB link%d VFAT2 TX:"%(link),  counters["glib_link%d_vfat2_tx_counter"%(link)])
            window.printLabel(0,  17+(i*5), 24, "GLIB link%d regs RX:"%(link),   counters["glib_link%d_reg_rx_counter"%(link)])
            window.printLabel(0,  18+(i*5), 24, "GLIB link%d regs TX:"%(link),   counters["glib_link%d_reg_tx_counter"%(link)])

            window.printLabel(27, 14+(i*5), 24, "OH link%d errors:"%(links[link]),      counters["oh_link%d_error_counter"%(links[link])])
            window.printLabel(27, 15+(i*5), 24, "OH link%d VFAT2 RX:"%(links[link]),    counters["oh_link%d_vfat2_rx_counter"%(links[link])])
            window.printLabel(27, 16+(i*5), 24, "OH link%d VFAT2 TX:"%(links[link]),    counters["oh_link%d_vfat2_tx_counter"%(links[link])])
            window.printLabel(27, 17+(i*5), 24, "OH link%d regs RX:"%(links[link]),     counters["oh_link%d_reg_rx_counter"%(links[link])])
            window.printLabel(27, 18+(i*5), 24, "OH link%d regs TX:"%(links[link]),     counters["oh_link%d_reg_tx_counter"%(links[link])])
        # Manage user input
        for i in range(0, 10000000):
            select = window.getChr()
            if (select == ord('q')): return -1
            elif (select == ord('s')): return 1
            elif (select == ord('r')): return 2
            elif (select == ord('d')): return 3

#########################################
#   Change the parameters               #
#########################################

def setRegistersWindow():
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Changing the system's registers", "Subtitle")
    window.printLine(3, "You can now change the value of the registers, press [Enter] to keep the", "Highlight")
    window.printLine(4, "current value. The recommended value is shown in parentheses and the range", "Highlight")
    window.printLine(5, "of accepted values in brackets.", "Highlight")
    window.printLine(-1, "Enter a new value for each register ([Enter] to use the current value).", "Options")
    # Go to blocking mode
    window.enableBlocking()
    # Get all the values to show
    systemRegisters = glib.saveSystem()
    #
    sbitSelect        = window.inputIntShifted(0, 7, "SBit VFAT2 select [8-13]:",      2, 8, 13, (systemRegisters["oh_sbit_select"] + 8))
    triggerSourceOH   = window.inputIntShifted(0,  8, "OH Trg src (2) [0-2]:",     1, 0, 2, systemRegisters["oh_trigger_source"])
    triggerSourceGLIB = window.inputIntShifted(0,  9, "GLIB Trg src (2) [0-2]:",   1, 0, 2, systemRegisters["glib_trigger_source"])
    vfat2Clk          = window.inputIntShifted(0, 10, "VFAT2 Clock (1) [0-1]:",    1, 0, 1, systemRegisters["oh_vfat2_src_select"])
    cdceClk           = window.inputIntShifted(0, 11, "CDCE Clock (1) [0-1]:",     1, 0, 1, systemRegisters["oh_cdce_src_select"])
    vfat2Fallback     = window.inputIntShifted(0, 13, "VFAT2 fallback (0) [0-1]:", 1, 0, 1, systemRegisters["oh_vfat2_fallback"])
    cdceFallback      = window.inputIntShifted(0, 14, "CDCE fallback (0) [0-1]:",  1, 0, 1, systemRegisters["oh_cdce_fallback"])
    #
    window.printLine(-1, "Apply the changes? [y]es, [n]o", "Options")
    #
    while (True):
        pressedKey = window.getChr()
        if (pressedKey == ord('n')): return
        elif (pressedKey == ord('y')): break
    #
    if (triggerSourceOH != systemRegisters["oh_trigger_source"]):
	    glib.setOHTriggerSource(triggerSourceOH)
    if (triggerSourceGLIB != systemRegisters["glib_trigger_source"]):
	    glib.setGLIBTriggerSource(triggerSourceGLIB)
    if (sbitSelect != systemRegisters["oh_sbit_select"]):
	    glib.setSBitSource(sbitSelect - 8)
    if (vfat2Clk != systemRegisters["oh_vfat2_src_select"]):
	    glib.setVFATClkSrc(vfat2Clk)
    if (cdceClk  != systemRegisters["oh_cdce_src_select"]):
	    glib.setCDCEClkSrc(cdceClk)
    if (vfat2Fallback != systemRegisters["oh_vfat2_fallback"]):
	    glib.setVFATClkBkp(vfat2Fallback)
    if (cdceFallback  != systemRegisters["oh_cdce_fallback"]):
	    glib.setCDCEClkBkp(cdceFallback)
    #
    newRegisters = glib.saveSystem()
    # Log
    save = Save("log")
    save.writeLine("Changed parameters of the system")
    save.writeLine("--- Old configuration ---")
    save.writeDict(systemRegisters)
    save.writeLine("--- New configuration ---")
    save.writeDict(newRegisters)
    #
    window.printLine(-1, "Settings applied!", "Success")
    #
    time.sleep(0.5)

#########################################
#   Reset the counters                  #
#########################################

def resetCountersWindow():
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Resetting the system's counters", "Subtitle")
    window.printLine(3, "Waiting for confirmation before resetting the system's counters.", "Highlight")
    window.printLine(-1, "Reset the counters? [y]es, [n]o", "Options")
    # Go to non-blocking mode
    window.enableBlocking()
    #
    while (True):
        pressedKey = window.getChr()
        if (pressedKey == ord('n')): return
        elif (pressedKey == ord('y')): break
    #
    glib.resetCounters()
    #
    window.printLine(-1, "Counters reset!", "Success")
    #
    time.sleep(0.5)

#########################################
#   Set defaults                        #
#########################################

def setDefaultsWindow():
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Setting the system's registers to their default value", "Subtitle")
    window.printLine(3, "Waiting for confirmation before setting the system's registers.", "Highlight")
    window.printLine(-1, "Set the registers to their default value? [y]es, [n]o", "Options")
    # Go to non-blocking mode
    window.enableBlocking()
    #
    while (True):
        pressedKey = window.getChr()
        if (pressedKey == ord('n')): return
        elif (pressedKey == ord('y')): break
    #
    systemRegisters = glib.saveSystem()
    #
    glib.systemDefault()
    #
    newRegisters = glib.saveSystem()
    # Log
    save = Save("log")
    save.writeLine("Changed parameters of the system")
    save.writeLine("--- Old configuration ---")
    save.writeDict(systemRegisters)
    save.writeLine("--- New configuration ---")
    save.writeDict(newRegisters)
    #
    window.printLine(-1, "Registers set!", "Success")
    #
    time.sleep(0.5)

#########################################
#   Main program                        #
#########################################
introWindow()
#
while (True):
    nextState = mainWindow()
    if (nextState == -1): break
    elif (nextState == 1): setRegistersWindow()
    elif (nextState == 2): resetCountersWindow()
    elif (nextState == 3): setDefaultsWindow()

# Close window
window.close()
