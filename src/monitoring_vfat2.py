# System imports
import time
from kernel import *

# Navigate between windows
nextWindow = 0

# Create window
window = Window("VFAT2 Monitoring")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

#########################################
#   Main window: view registers         #
#########################################

def mainWindow(vfat2ID):
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Monitoring VFAT2 #"+str(vfat2ID), "Info")
    window.printLine(2, "Current value of the registers: values that appear in red differ from the", "Warning")
    window.printLine(3, "recommended value for data tacking (in parentheses).", "Warning")
    window.printLine(-1, "[q]uit, [s]et the registers, [c]hange VFAT2", "Info")
    # Go to non-blocking mode
    window.disableBlocking()
    # Stay in this window until command select
    while (True):
        # Get all the values to show
        vfat2Registers = glib.saveVFAT2(vfat2ID)
        # Check that data is present
        if (len(vfat2Registers) != 0):
            # Clear line
            window.clear(4, 2)
            #
            hitcounter = (vfat2Registers["hitcount2"] << 16) | (vfat2Registers["hitcount1"] << 8) | vfat2Registers["hitcount0"]
            #
            window.printLabel(0, 5, 24, "Control 0 (55):", vfat2Registers["ctrl0"], ("Error" if (vfat2Registers["ctrl0"] != 55) else "Success"))
            window.printLabel(0, 6, 24, "Control 1 (0):", vfat2Registers["ctrl1"], ("Error" if (vfat2Registers["ctrl1"] != 0) else "Success"))
            window.printLabel(0, 7, 24, "Control 2 (48):", vfat2Registers["ctrl2"], ("Error" if (vfat2Registers["ctrl2"] != 48) else "Success"))
            window.printLabel(0, 8, 24, "Control 3 (0):", vfat2Registers["ctrl3"], ("Error" if (vfat2Registers["ctrl3"] != 0) else "Success"))
            window.printLabel(0, 9, 24, "Chip ID 0:", vfat2Registers["chipid0"])
            window.printLabel(0, 10, 24, "Chip ID 1:", vfat2Registers["chipid1"])
            window.printLabel(27, 5, 24, "IPreampIn (168):", vfat2Registers["ipreampin"], ("Error" if (vfat2Registers["ipreampin"] != 168) else "Success"))
            window.printLabel(27, 6, 24, "IPreampFeed (80):", vfat2Registers["ipreampfeed"], ("Error" if (vfat2Registers["ipreampfeed"] != 80) else "Success"))
            window.printLabel(27, 7, 24, "IPreampOut (150):", vfat2Registers["ipreampout"], ("Error" if (vfat2Registers["ipreampout"] != 150) else "Success"))
            window.printLabel(27, 8, 24, "IShaper (150):", vfat2Registers["ishaper"], ("Error" if (vfat2Registers["ishaper"] != 150) else "Success"))
            window.printLabel(27, 9, 24, "IShaperFeed (100):", vfat2Registers["ishaperfeed"], ("Error" if (vfat2Registers["ishaperfeed"] != 100) else "Success"))
            window.printLabel(27, 10, 24, "IComp (75):", vfat2Registers["icomp"], ("Error" if (vfat2Registers["icomp"] != 75) else "Success"))
            window.printLabel(54, 5, 24, "VThreshold 1:", vfat2Registers["vthreshold1"])
            window.printLabel(54, 6, 24, "VThreshold 2 (0):", vfat2Registers["vthreshold2"], ("Error" if (vfat2Registers["vthreshold2"] != 0) else "Success"))
            window.printLabel(54, 7, 24, "VCal:", vfat2Registers["vcal"])
            window.printLabel(54, 8, 24, "Calphase:", vfat2Registers["calphase"])
            window.printLabel(54, 9, 24, "Latency (10):", vfat2Registers["latency"], ("Error" if (vfat2Registers["latency"] != 10) else "Success"))
            window.printLabel(54, 10, 24, "Hit counter:", hitcounter)
        # Manage user input
        for i in range(0, 10000000):
            select = window.getChr()
            if (select == ord('q')): return -1
            elif (select == ord('s')): return 1
            elif (select == ord('c')): return 2

#########################################
#   Change the parameters               #
#########################################

def setRegistersWindow(vfat2ID):
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Changing registers of VFAT2 #"+str(vfat2ID), "Info")
    window.printLine(2, "You can now change the value of the registers, press [Enter] to keep the", "Warning")
    window.printLine(3, "current value.", "Warning")
    # Go to blocking mode
    window.enableBlocking()
    # Get all the values to show
    vfat2Registers = glib.saveVFAT2(vfat2ID)
    #
    ctrl0 = window.inputIntShifted(0, 5, "Control 0 (55):", 3, 0, 255, vfat2Registers["ctrl0"])
    ctrl1 = window.inputIntShifted(0, 6, "Control 1 (0):", 3, 0, 255, vfat2Registers["ctrl1"])
    ctrl2 = window.inputIntShifted(0, 7, "Control 2 (48):", 3, 0, 255, vfat2Registers["ctrl2"])
    ctrl3 = window.inputIntShifted(0, 8, "Control 3 (0):", 3, 0, 255, vfat2Registers["ctrl3"])
    ipreampin = window.inputIntShifted(27, 5, "IPreampIn (168):", 3, 0, 255, vfat2Registers["ipreampin"])
    ipreampfeed = window.inputIntShifted(27, 6, "IPreampFeed (80):", 3, 0, 255, vfat2Registers["ipreampfeed"])
    ipreampout = window.inputIntShifted(27, 7, "IPreampOut (150):", 3, 0, 255, vfat2Registers["ipreampout"])
    ishaper = window.inputIntShifted(27, 8, "IShaper (150):", 3, 0, 255, vfat2Registers["ishaper"])
    ishaperfeed = window.inputIntShifted(27, 9, "IShaperFeed (100):", 3, 0, 255, vfat2Registers["ishaperfeed"])
    icomp = window.inputIntShifted(27, 10, "IComp (75):", 3, 0, 255, vfat2Registers["icomp"])
    vthreshold1 = window.inputIntShifted(54, 5, "VThreshold 1:", 3, 0, 255, vfat2Registers["vthreshold1"])
    vthreshold2 = window.inputIntShifted(54, 6, "VThreshold 2 (0):", 3, 0, 255, vfat2Registers["vthreshold2"])
    vcal = window.inputIntShifted(54, 7, "VCal:", 3, 0, 255, vfat2Registers["vcal"])
    calphase = window.inputIntShifted(54, 8, "Calphase:", 3, 0, 255, vfat2Registers["calphase"])
    latency = window.inputIntShifted(54, 9, "Latency (10):", 3, 0, 255, vfat2Registers["latency"])
    #
    window.printLine(-1, "appl[y] the changes, ig[n]ore the changes", "Info")
    #
    while (True):
        pressedKey = window.getChr()
        if (pressedKey == ord('n')): return
        elif (pressedKey == ord('y')): break
    #
    if (ctrl0 != vfat2Registers["ctrl0"]): glib.setVFAT2(vfat2ID, "ctrl0", ctrl0)
    if (ctrl1 != vfat2Registers["ctrl1"]): glib.setVFAT2(vfat2ID, "ctrl1", ctrl2)
    if (ctrl2 != vfat2Registers["ctrl2"]): glib.setVFAT2(vfat2ID, "ctrl2", ctrl2)
    if (ctrl3 != vfat2Registers["ctrl3"]): glib.setVFAT2(vfat2ID, "ctrl3", ctrl3)
    if (ipreampin != vfat2Registers["ipreampin"]): glib.setVFAT2(vfat2ID, "ipreampin", ipreampin)
    if (ipreampfeed != vfat2Registers["ipreampfeed"]): glib.setVFAT2(vfat2ID, "ipreampfeed", ipreampfeed)
    if (ipreampout != vfat2Registers["ipreampout"]): glib.setVFAT2(vfat2ID, "ipreampout", ipreampout)
    if (ishaper != vfat2Registers["ishaper"]): glib.setVFAT2(vfat2ID, "ishaper", ishaper)
    if (ishaperfeed != vfat2Registers["ishaperfeed"]): glib.setVFAT2(vfat2ID, "ishaperfeed", ishaperfeed)
    if (icomp != vfat2Registers["icomp"]): glib.setVFAT2(vfat2ID, "icomp", icomp)
    if (vthreshold1 != vfat2Registers["vthreshold1"]): glib.setVFAT2(vfat2ID, "vthreshold1", vthreshold1)
    if (vthreshold2 != vfat2Registers["vthreshold2"]): glib.setVFAT2(vfat2ID, "vthreshold2", vthreshold2)
    if (vcal != vfat2Registers["vcal"]): glib.setVFAT2(vfat2ID, "vcal", vcal)
    if (calphase != vfat2Registers["calphase"]): glib.setVFAT2(vfat2ID, "calphase", calphase)
    if (latency != vfat2Registers["latency"]): glib.setVFAT2(vfat2ID, "latency", latency)
    #
    newRegisters = glib.saveVFAT2(vfat2ID)
    #
    save = Save("log")
    save.writeLine("Changed VFAT2 parameters")
    save.writePair("VFAT2", vfat2ID)
    save.writeDict(newRegisters)
    #
    window.printLine(-1, "Settings applied!", "Success")
    #
    time.sleep(2)

#########################################
#   Main program                        #
#########################################

isConnected = False
# Program loop
while (True):
    if (isConnected == False):
        # Clear the screen
        window.clear()
        # Go to blocking mode
        window.enableBlocking()
        # Select the VFAT2
        vfat2ID = window.inputInt(1, "Select a VFAT2 to monitor [8-13]:", 2, 8, 13, 8)
        # Test if VFAT2 is present
        if (glib.isVFAT2Present(vfat2ID) == False):
            # Clear line
            window.clear()
            # Error
            window.printLine(1, "The selected VFAT2 is not present!", "Error")
            # Timeout
            time.sleep(3)
        else: isConnected = True
    else:
        nextState = mainWindow(vfat2ID)

        if (nextState == -1): break
        elif (nextState == 1): setRegistersWindow(vfat2ID)
        elif (nextState == 2): isConnected = False

# Wait for quit

# Close window
window.close()
