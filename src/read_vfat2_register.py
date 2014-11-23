# System imports
from system import *

# Create window
window = Window("Read a VFAT2's register")
# Get GLIB access

glib = GLIB()
glib.setWindow(window)

# Get a VFAT2 number
window.printBox(0, 4, 37, "Select the VFAT2 to read from [8-13]:", "Default", "left")
inputData = window.getInt(38, 4, 2)
VFAT2 = 8 if (inputData < 8 or inputData > 13) else inputData
window.printBox(37, 4, 3, str(VFAT2), "Input", "left")

# Test if VFAT2 is present
if (glib.isVFAT2(VFAT2) == False):
    # Error
    window.printLine(6, "The selected VFAT2 is not present!", "Error", "center")

else:

    # Get a register address
    window.printBox(0, 6, 26, "Register address [0-150]:", "Default", "left")
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

    inputData = window.getInt(26, 6, 3)
    regId = 0 if (inputData < 0 or inputData > 150) else inputData
    window.printBox(26, 6, 3, str(regId), "Input", "left")

    # Change the register
    if (regId == 0):
        regValue = glib.getVFAT2(VFAT2, "ctrl0")
    elif (regId == 1):
        regValue = glib.getVFAT2(VFAT2, "ctrl1")
    elif (regId == 2):
        regValue = glib.getVFAT2(VFAT2, "ipreampin")
    elif (regId == 3):
        regValue = glib.getVFAT2(VFAT2, "ipreampfeed")
    elif (regId == 4):
        regValue = glib.getVFAT2(VFAT2, "ipreampout")
    elif (regId == 5):
        regValue = glib.getVFAT2(VFAT2, "ishaper")
    elif (regId == 6):
        regValue = glib.getVFAT2(VFAT2, "ishaperfeed")
    elif (regId == 7):
        regValue = glib.getVFAT2(VFAT2, "icomp")
    elif (regId == 8):
        regValue = glib.getVFAT2(VFAT2, "chipid0")
    elif (regId == 9):
        regValue = glib.getVFAT2(VFAT2, "chipid1")
    elif (regId == 10):
        regValue = glib.getVFAT2(VFAT2, "upsetreg")
    elif (regId == 11):
        regValue = glib.getVFAT2(VFAT2, "hitcount0")
    elif (regId == 12):
        regValue = glib.getVFAT2(VFAT2, "hitcount1")
    elif (regId == 13):
        regValue = glib.getVFAT2(VFAT2, "hitcount2")
    elif (regId == 14):
        regValue = glib.getVFAT2(VFAT2, "extregpointer")
    elif (regId == 15):
        regValue = glib.getVFAT2(VFAT2, "extregdata")
    elif (regId == 16):
        regValue = glib.getVFAT2(VFAT2, "latency")
    elif (regId >= 17 or regId <= 144):
        regValue = glib.getVFAT2(VFAT2, "channel" + str(regId - 16))
    elif (regId == 145):
        regValue = glib.getVFAT2(VFAT2, "vcal")
    elif (regId == 146):
        regValue = glib.getVFAT2(VFAT2, "vthreshold1")
    elif (regId == 147):
        regValue = glib.getVFAT2(VFAT2, "vthreshold2")
    elif (regId == 148):
        regValue = glib.getVFAT2(VFAT2, "calphase")
    elif (regId == 149):
        regValue = glib.getVFAT2(VFAT2, "ctrl2")
    elif (regId == 150):
        regValue = glib.getVFAT2(VFAT2, "ctrl3")

    # Success
    window.printLine(14, "Read value: " + hex(regValue), "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
