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
window = Window("VFAT2 Monitoring")

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
    window.printLine(3, "This program allows you to control and monitor the VFAT2s.")
    window.printLine(5, "You will be asked to enter the number of the VFAT2 on the GEB that you want to")
    window.printLine(6, "monitor. Once the system is connected, it will show you the values written")
    window.printLine(7, "in the various registers and update them every few seconds.")
    window.printLine(9, "The list of actions that can be performed are listed on the bottom")
    window.printLine(10, "of the screen. Once connected, here are the possible actions:")
    window.printLine(11, "Press [c] to switch to another VFAT2 on the GEB.")
    window.printLine(12, "Press [s] to change the value of the registers.")
    window.printLine(13, "Press [d] to set the registers to their default value.")
    window.printLine(14, "Press [q] to quit the program.")
    window.printLine(15, "As you can see, when a key performs an action, it is placed between brackets.")
    window.printLine(17, "You can always exit the program by pressing [Ctrl+C].")
    window.printLine(-2, "Hint: here is what to do next (possible actions are always shown here)")
    window.printLine(-1, "Press [c] to continue.", "Options")
    window.waitForKey("c")

#########################################
#   Main window: view registers         #
#########################################

def mainWindow(vfat2ID):
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Monitoring VFAT2 #"+str(vfat2ID), "Subtitle")
    window.printLine(3, "Current values of the registers: values that appear in red differ from the", "Highlight")
    window.printLine(4, "recommended value for data tacking (in parentheses).", "Highlight")
    window.printLine(-1, "Actions: [q]uit, [s]et the registers, [c]hange VFAT2, [d]efault values", "Options")
    # Go to non-blocking mode
    window.disableBlocking()
    # Stay in this window until command select
    while (True):
        # Get all the values to show
        vfat2Registers = glib.saveVFAT2(vfat2ID)

        statusVFAT2 = [0 for x in range(24)]

        for i in range(0, 24):
	    if (0 not in links.keys()):
		if (i < 8):
                    continue
	    if (1 not in links.keys()):
		if ((i > 7) and (i < 16)):
                    continue
	    if (2 not in links.keys()):
		if (i > 15):
                    continue
	    # now only chips we could reasonably talk to
            if (glib.isVFAT2Present(i)):
                statusVFAT2[i] = 2 if glib.isVFAT2Running(i) else 1
            else:
                statusVFAT2[i] = 0

        # Check that data is present
        if (len(vfat2Registers) != 0):
            # Clear line
            window.clear(5, 1)
            #
            hitcounter = (vfat2Registers["hitcount2"] << 16) | (vfat2Registers["hitcount1"] << 8) | vfat2Registers["hitcount0"]
            #
            window.printLabel(0, 6, 24, "Control 0 (55):", vfat2Registers["ctrl0"], ("Error" if (vfat2Registers["ctrl0"] != 55) else "Success"))
            window.printLabel(0, 7, 24, "Control 1 (0) :", vfat2Registers["ctrl1"], ("Error" if (vfat2Registers["ctrl1"] != 0) else "Success"))
            window.printLabel(0, 8, 24, "Control 2 (48):", vfat2Registers["ctrl2"], ("Error" if (vfat2Registers["ctrl2"] != 48) else "Success"))
            window.printLabel(0, 9, 24, "Control 3 (0) :", vfat2Registers["ctrl3"], ("Error" if (vfat2Registers["ctrl3"] != 0) else "Success"))
            window.printLabel(0, 10, 24, "Chip ID      :", hex((vfat2Registers["chipid1"]<<8)|vfat2Registers["chipid0"]))
	    
            window.printLabel(27, 6, 24, "IPreampIn (168):", vfat2Registers["ipreampin"], ("Error" if (vfat2Registers["ipreampin"] != 168) else "Success"))
            window.printLabel(27, 7, 24, "IPreampFeed (80):", vfat2Registers["ipreampfeed"], ("Error" if (vfat2Registers["ipreampfeed"] != 80) else "Success"))
            window.printLabel(27, 8, 24, "IPreampOut (150):", vfat2Registers["ipreampout"], ("Error" if (vfat2Registers["ipreampout"] != 150) else "Success"))
            window.printLabel(27, 9, 24, "IShaper (150):", vfat2Registers["ishaper"], ("Error" if (vfat2Registers["ishaper"] != 150) else "Success"))
            window.printLabel(27, 10, 24, "IShaperFeed (100):", vfat2Registers["ishaperfeed"], ("Error" if (vfat2Registers["ishaperfeed"] != 100) else "Success"))
            window.printLabel(27, 11, 24, "IComp (75):", vfat2Registers["icomp"], ("Error" if (vfat2Registers["icomp"] != 75) else "Success"))
            window.printLabel(54, 6, 24, "VThreshold 1:", vfat2Registers["vthreshold1"])
            window.printLabel(54, 7, 24, "VThreshold 2 (0):", vfat2Registers["vthreshold2"], ("Error" if (vfat2Registers["vthreshold2"] != 0) else "Success"))
            window.printLabel(54, 8, 24, "VCal:", vfat2Registers["vcal"])
            window.printLabel(54, 9, 24, "Calphase:", vfat2Registers["calphase"])
            window.printLabel(54, 10, 24, "Latency (20):", vfat2Registers["latency"], ("Error" if (vfat2Registers["latency"] != 20) else "Success"))
            window.printLabel(54, 11, 24, "Hit counter:", hitcounter)

            window.printLine(13, "Status of the other VFAT2s", "Highlight")

            for i in range(0, 24):
                if (statusVFAT2[i] == 2):
                    window.printBox((i % 8) * 8, (15 + i / 8), 7, "#"+str(i)+" On", "Success")
                elif (statusVFAT2[i] == 1):
                    window.printBox((i % 8) * 8, (15 + i / 8), 7, "#"+str(i)+" Off", "Warning")
                else:
                    window.printBox((i % 8) * 8, (15 + i / 8), 7, "#"+str(i)+" XXX", "Error")

        # Manage user input
        for i in range(0, 10000000):
            select = window.getChr()
            if (select == ord('q')): return -1
            elif (select == ord('s')): return 1
            elif (select == ord('c')): return 2
            elif (select == ord('d')): return 3

#########################################
#   Change the parameters               #
#########################################

def setRegistersWindow(vfat2ID):
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Changing VFAT2 #"+str(vfat2ID)+"'s registers", "Subtitle")
    window.printLine(3, "You can now change the value of the registers, press [Enter] to keep the", "Highlight")
    window.printLine(4, "current value. The recommended value is shown in parentheses and the range", "Highlight")
    window.printLine(5, "of accepted values in brackets.", "Highlight")
    window.printLine(-1, "Enter a new value for each register ([Enter] to use the current value).", "Options")
    # Go to blocking mode
    window.enableBlocking()
    # Get all the values to show
    vfat2Registers = glib.saveVFAT2(vfat2ID)
    #
    ctrl0 = window.inputIntShifted(0,  7, "Control 0 (55) [0-255]:", 3, 0, 255, vfat2Registers["ctrl0"])
    ctrl1 = window.inputIntShifted(0,  8, "Control 1 (0) [0-255]:",  3, 0, 255, vfat2Registers["ctrl1"])
    ctrl2 = window.inputIntShifted(0,  9, "Control 2 (48) [0-255]:", 3, 0, 255, vfat2Registers["ctrl2"])
    ctrl3 = window.inputIntShifted(0, 10, "Control 3 (0) [0-255]:",  3, 0, 255, vfat2Registers["ctrl3"])
    ipreampin   = window.inputIntShifted(0,  12, "IPreampIn (168) [0-255]:",   3, 0, 255, vfat2Registers["ipreampin"])
    ipreampfeed = window.inputIntShifted(0,  13, "IPreampFeed (80) [0-255]:",  3, 0, 255, vfat2Registers["ipreampfeed"])
    ipreampout  = window.inputIntShifted(0,  14, "IPreampOut (150) [0-255]:",  3, 0, 255, vfat2Registers["ipreampout"])
    ishaper     = window.inputIntShifted(0,  15, "IShaper (150) [0-255]:",     3, 0, 255, vfat2Registers["ishaper"])
    ishaperfeed = window.inputIntShifted(0,  16, "IShaperFeed (100) [0-255]:", 3, 0, 255, vfat2Registers["ishaperfeed"])
    icomp       = window.inputIntShifted(0,  17, "IComp (75) [0-255]:",        3, 0, 255, vfat2Registers["icomp"])
    vthreshold1 = window.inputIntShifted(40,  7, "VThreshold 1 [0-255]:",      3, 0, 255, vfat2Registers["vthreshold1"])
    vthreshold2 = window.inputIntShifted(40,  8, "VThreshold 2 (0) [0-255]:",  3, 0, 255, vfat2Registers["vthreshold2"])
    vcal        = window.inputIntShifted(40, 10, "VCal [0-255]:",              3, 0, 255, vfat2Registers["vcal"])
    calphase    = window.inputIntShifted(40, 11, "Calphase [0-255]:",          3, 0, 255, vfat2Registers["calphase"])
    latency     = window.inputIntShifted(40, 13, "Latency (20) [0-255]:",      3, 0, 255, vfat2Registers["latency"])
    #
    window.printLine(-1, "Apply the changes? [y]es, [n]o", "Options")
    #
    while (True):
        pressedKey = window.getChr()
        if (pressedKey == ord('n')): return
        elif (pressedKey == ord('y')): break
    #
    if (ctrl0       != vfat2Registers["ctrl0"]):       glib.setVFAT2(vfat2ID, "ContReg0",    ctrl0)
    if (ctrl1       != vfat2Registers["ctrl1"]):       glib.setVFAT2(vfat2ID, "ContReg1",    ctrl1)
    if (ctrl2       != vfat2Registers["ctrl2"]):       glib.setVFAT2(vfat2ID, "ContReg2",    ctrl2)
    if (ctrl3       != vfat2Registers["ctrl3"]):       glib.setVFAT2(vfat2ID, "ContReg3",    ctrl3)
    if (ipreampin   != vfat2Registers["ipreampin"]):   glib.setVFAT2(vfat2ID, "IPreampIn",   ipreampin)
    if (ipreampfeed != vfat2Registers["ipreampfeed"]): glib.setVFAT2(vfat2ID, "IPreampFeed", ipreampfeed)
    if (ipreampout  != vfat2Registers["ipreampout"]):  glib.setVFAT2(vfat2ID, "IPreampOut",  ipreampout)
    if (ishaper     != vfat2Registers["ishaper"]):     glib.setVFAT2(vfat2ID, "IShaper",     ishaper)
    if (ishaperfeed != vfat2Registers["ishaperfeed"]): glib.setVFAT2(vfat2ID, "IShaperFeed", ishaperfeed)
    if (icomp       != vfat2Registers["icomp"]):       glib.setVFAT2(vfat2ID, "IComp",       icomp)
    if (vthreshold1 != vfat2Registers["vthreshold1"]): glib.setVFAT2(vfat2ID, "VThreshold1", vthreshold1)
    if (vthreshold2 != vfat2Registers["vthreshold2"]): glib.setVFAT2(vfat2ID, "VThreshold2", vthreshold2)
    if (vcal        != vfat2Registers["vcal"]):        glib.setVFAT2(vfat2ID, "VCal",        vcal)
    if (calphase    != vfat2Registers["calphase"]):    glib.setVFAT2(vfat2ID, "CalPhase",    calphase)
    if (latency     != vfat2Registers["latency"]):     glib.setVFAT2(vfat2ID, "Latency",     latency)
    #
    newRegisters = glib.saveVFAT2(vfat2ID)
    # Log
    save = Save("log")
    save.writeLine("Changed parameters of VFAT2 #"+str(vfat2ID))
    save.writeLine("--- Old configuration ---")
    save.writeDict(vfat2Registers)
    save.writeLine("--- New configuration ---")
    save.writeDict(newRegisters)
    #
    window.printLine(-1, "Settings applied!", "Success")
    #
    time.sleep(0.5)

#########################################
#   Set defaults                        #
#########################################

def setDefaultsWindow(vfat2ID):
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Setting VFAT2 #"+str(vfat2ID)+"'s registers to their default value", "Subtitle")
    window.printLine(3, "Waiting for confirmation before setting VFAT2 #"+str(vfat2ID)+"'s registers.", "Highlight")
    window.printLine(-1, "Set the registers to their default value? [y]es, [n]o", "Options")
    # Go to non-blocking mode
    window.enableBlocking()
    #
    while (True):
        pressedKey = window.getChr()
        if (pressedKey == ord('n')): return
        elif (pressedKey == ord('y')): break
    #
    vfat2Registers = glib.saveVFAT2(vfat2ID)
    #
    glib.setVFAT2(vfat2ID, "ContReg0",     55)
    glib.setVFAT2(vfat2ID, "ContReg1",      0)
    glib.setVFAT2(vfat2ID, "ContReg2",     48)
    glib.setVFAT2(vfat2ID, "ContReg3",      0)
    glib.setVFAT2(vfat2ID, "IPreampIn",   168)
    glib.setVFAT2(vfat2ID, "IPreampFeed",  80)
    glib.setVFAT2(vfat2ID, "IPreampOut",  150)
    glib.setVFAT2(vfat2ID, "IShaper",     150)
    glib.setVFAT2(vfat2ID, "IShaperFeed", 100)
    glib.setVFAT2(vfat2ID, "IComp",        75)
    glib.setVFAT2(vfat2ID, "VThreshold1",  15)
    glib.setVFAT2(vfat2ID, "VThreshold2",   0)
    glib.setVFAT2(vfat2ID, "VCal",          0)
    glib.setVFAT2(vfat2ID, "CalPhase",      0)
    glib.setVFAT2(vfat2ID, "Latency",      20)
    #
    newRegisters = glib.saveVFAT2(vfat2ID)
    # Log
    save = Save("log")
    save.writeLine("Changed parameters of VFAT2 #"+str(vfat2ID))
    save.writeLine("--- Old configuration ---")
    save.writeDict(vfat2Registers)
    save.writeLine("--- New configuration ---")
    save.writeDict(newRegisters)
    #
    window.printLine(-1, "Registers set!", "Success")
    #
    time.sleep(0.5)

#########################################
#   Main program                        #
#########################################

isConnected = False
# Show the intro
introWindow()
# Program loop
while (True):
    if (isConnected == False):
        # Clear the screen
        window.clear()
        # Go to blocking mode
        window.enableBlocking()
        # Select the VFAT2
        window.printLine(1, "VFAT2 selection", "Subtitle")
        window.printLine(-1, "You have to specify which VFAT2 you want to monitor.", "Options")
        vfat2ID = window.inputInt(3, "Select the VFAT2 to monitor [0-23]:", 2, 0, 23, 0)
        # Test if VFAT2 is present
        if (glib.isVFAT2Present(vfat2ID) == False):
            # Clear line
            window.clear()
            # Error
            window.printLine(3, "The selected VFAT2 is not present!", "Error")
            # Timeout
            time.sleep(0.5)
        else: isConnected = True
    else:
        nextState = mainWindow(vfat2ID)

        if (nextState == -1): break
        elif (nextState == 1): setRegistersWindow(vfat2ID)
        elif (nextState == 2): isConnected = False
        elif (nextState == 3): setDefaultsWindow(vfat2ID)

# Close window
window.close()
