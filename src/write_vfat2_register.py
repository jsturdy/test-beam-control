# System imports
from system import *

# Create window
window = Window("Write in a VFAT2's register")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Get a VFAT2 number
vfat2ID = window.inputInt(4, "Select the VFAT2 to read from [8-13]:", 2, 8, 13, 8)

# Test if VFAT2 is present
if (glib.isVFAT2(vfat2ID) == False):
    # Error
    window.printLine(6, "The selected VFAT2 is not present!", "Error", "center")
#
else:
    # Get a register address
    window.printBox(0, 7, 20, "0: Control 0")
    window.printBox(20, 7, 20, "1: Control 1")
    window.printBox(40, 7, 20, "2: IPreampIn")
    window.printBox(60, 7, 20, "3: IPreampFeed")
    window.printBox(0, 8, 20, "4: IPreampOut")
    window.printBox(20, 8, 20, "5: IShaper")
    window.printBox(40, 8, 20, "6: IShaperFeed")
    window.printBox(60, 8, 20, "7: Icomp")
    window.printBox(0, 9, 20, "8: ChipID 0")
    window.printBox(20, 9, 20, "9: ChipID 1")
    window.printBox(40, 9, 20, "10: UpsetRegister")
    window.printBox(60, 9, 20, "11: Hit counter 0")
    window.printBox(0, 10, 20, "12: Hit counter 1")
    window.printBox(20, 10, 20, "13: Hit counter 2")
    window.printBox(40, 10, 20, "14: Pointer register")
    window.printBox(60, 10, 20, "15: Pointer data")
    window.printBox(0, 11, 20, "16: Latency")
    window.printBox(20, 11, 20, "17-144: Channels")
    window.printBox(40, 11, 20, "145: VCal")
    window.printBox(60, 11, 20, "146: VTHreshold1")
    window.printBox(0, 12, 20, "147: VTHreshold2")
    window.printBox(20, 12, 20, "148: Calphase")
    window.printBox(40, 12, 20, "149: Control 2")
    window.printBox(60, 12, 20, "150: Control 3")
    regId = window.inputInt(6, "Register address [0-150]:", 3, 0, 150, 0)

    regValue = window.inputInt(14, "Register value [0-255]:", 3, 0, 255, 0)

    window.printLine(16, "Press [s] to apply the changes.", "Info", "center")
    window.waitForKey("s")

    # Change the register
    if (regId == 0):
        glib.setVFAT2(vfat2ID, "ctrl0", regValue)
    elif (regId == 1):
        glib.setVFAT2(vfat2ID, "ctrl1", regValue)
    elif (regId == 2):
        glib.setVFAT2(vfat2ID, "ipreampin", regValue)
    elif (regId == 3):
        glib.setVFAT2(vfat2ID, "ipreampfeed", regValue)
    elif (regId == 4):
        glib.setVFAT2(vfat2ID, "ipreampout", regValue)
    elif (regId == 5):
        glib.setVFAT2(vfat2ID, "ishaper", regValue)
    elif (regId == 6):
        glib.setVFAT2(vfat2ID, "ishaperfeed", regValue)
    elif (regId == 7):
        glib.setVFAT2(vfat2ID, "icomp", regValue)
    elif (regId == 8):
        glib.setVFAT2(vfat2ID, "chipid0", regValue)
    elif (regId == 9):
        glib.setVFAT2(vfat2ID, "chipid1", regValue)
    elif (regId == 10):
        glib.setVFAT2(vfat2ID, "upsetreg", regValue)
    elif (regId == 11):
        glib.setVFAT2(vfat2ID, "hitcount0", regValue)
    elif (regId == 12):
        glib.setVFAT2(vfat2ID, "hitcount1", regValue)
    elif (regId == 13):
        glib.setVFAT2(vfat2ID, "hitcount2", regValue)
    elif (regId == 14):
        glib.setVFAT2(vfat2ID, "extregpointer", regValue)
    elif (regId == 15):
        glib.setVFAT2(vfat2ID, "extregdata", regValue)
    elif (regId == 16):
        glib.setVFAT2(vfat2ID, "latency", regValue)
    elif (regId >= 17 or regId <= 144):
        glib.setVFAT2(vfat2ID, "channel" + str(regId - 16), regValue)
    elif (regId == 145):
        glib.setVFAT2(vfat2ID, "vcal", regValue)
    elif (regId == 146):
        glib.setVFAT2(vfat2ID, "vthreshold1", regValue)
    elif (regId == 147):
        glib.setVFAT2(vfat2ID, "vthreshold2", regValue)
    elif (regId == 148):
        glib.setVFAT2(vfat2ID, "calphase", regValue)
    elif (regId == 149):
        glib.setVFAT2(vfat2ID, "ctrl2", regValue)
    elif (regId == 150):
        glib.setVFAT2(vfat2ID, "ctrl3", regValue)

    glib.set("oh_resync", 1)

    # Success
    window.printLine(17, "Value written!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
