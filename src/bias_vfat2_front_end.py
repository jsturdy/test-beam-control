# System imports
from system import *

# Create window
window = Window("Bias a VFAT2's front-end")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Get a VFAT2 number
window.printBox(0, 4, 30, "Select a VFAT2 to scan [8-13]:", "Default", "left")
inputData = window.getInt(31, 4, 2)
VFAT2 = 8 if (inputData < 8 or inputData > 13) else inputData
window.printBox(31, 4, 3, str(VFAT2), "Input", "left")

# Test if VFAT2 is present
if (glib.isVFAT2(VFAT2) == False):
    # Error
    window.printLine(6, "The selected VFAT2 is not present!", "Error", "center")

else:

    # Description
    window.printLine(6, "Register    [Range] [Recommended] (Current)", "Default", "left")

    # Get a IPreampIn
    current = glib.getVFAT2(VFAT2, "ipreampin")
    window.printBox(0, 7, 33, "IPreampIn   [0-255] [168] (" + str(current) + "):", "Default", "left")
    inputData = window.getInt(33, 7, 3)
    IPreampIn = current if (inputData < 0 or inputData > 255) else inputData
    window.printBox(33, 7, 3, str(IPreampIn), "Input", "left")

    # Get a IPreampFeed
    current = glib.getVFAT2(VFAT2, "ipreampfeed")
    window.printBox(0, 8, 33, "IPreampFeed [0-255] [80]  (" + str(current) + "):", "Default", "left")
    inputData = window.getInt(33, 8, 3)
    IPreampFeed = current if (inputData < 0 or inputData > 255) else inputData
    window.printBox(33, 8, 3, str(IPreampFeed), "Input", "left")

    # Get a IPreampOut
    current = glib.getVFAT2(VFAT2, "ipreampout")
    window.printBox(0, 9, 33, "IPreampOut  [0-255] [150] (" + str(current) + "):", "Default", "left")
    inputData = window.getInt(33, 9, 3)
    IPreampOut = current if (inputData < 0 or inputData > 255) else inputData
    window.printBox(33, 9, 3, str(IPreampOut), "Input", "left")

    # Get a IShaper
    current = glib.getVFAT2(VFAT2, "ishaper")
    window.printBox(0, 10, 33, "IShaper     [0-255] [150] (" + str(current) + "):", "Default", "left")
    inputData = window.getInt(33, 10, 3)
    IShaper = current if (inputData < 0 or inputData > 255) else inputData
    window.printBox(33, 10, 3, str(IShaper), "Input", "left")

    # Get a IShaperFeed
    current = glib.getVFAT2(VFAT2, "ishaperfeed")
    window.printBox(0, 11, 33, "IShaperFeed [0-255] [100] (" + str(current) + "):", "Default", "left")
    inputData = window.getInt(33, 11, 3)
    IShaperFeed = current if (inputData < 0 or inputData > 255) else inputData
    window.printBox(33, 11, 3, str(IShaperFeed), "Input", "left")

    # Get a IComp
    current = glib.getVFAT2(VFAT2, "icomp")
    window.printBox(0, 12, 33, "IComp       [0-255] [120] (" + str(current) + "):", "Default", "left")
    inputData = window.getInt(33, 12, 3)
    IComp = current if (inputData < 0 or inputData > 255) else inputData
    window.printBox(33, 12, 3, str(IComp), "Input", "left")

    # Get a VThreshold1
    current = glib.getVFAT2(VFAT2, "vthreshold1")
    window.printBox(0, 13, 33, "VThreshold1 [0-255] [10]  (" + str(current) + "):", "Default", "left")
    inputData = window.getInt(33, 13, 3)
    VThreshold1 = current if (inputData < 0 or inputData > 255) else inputData
    window.printBox(33, 13, 3, str(VThreshold1), "Input", "left")

    # Get a VThreshold2
    current = glib.getVFAT2(VFAT2, "vthreshold2")
    window.printBox(0, 14, 33, "VThreshold2 [0-255] [0]   (" + str(current) + "):", "Default", "left")
    inputData = window.getInt(33, 14, 3)
    VThreshold2 = current if (inputData < 0 or inputData > 255) else inputData
    window.printBox(33, 14, 3, str(VThreshold2), "Input", "left")

    window.printLine(16, "Press [s] to bias the front-end.", "Info", "center")
    window.waitForKey("s")

    # Bias front-end
    glib.setVFAT2(VFAT2, "ipreampin", IPreampIn)
    glib.setVFAT2(VFAT2, "ipreampfeed", IPreampFeed)
    glib.setVFAT2(VFAT2, "ipreampout", IPreampOut)
    glib.setVFAT2(VFAT2, "ishaper", IShaper)
    glib.setVFAT2(VFAT2, "ishaperfeed", IShaperFeed)
    glib.setVFAT2(VFAT2, "icomp", IComp)
    glib.setVFAT2(VFAT2, "vthreshold1", VThreshold1)
    glib.setVFAT2(VFAT2, "vthreshold2", VThreshold2)
    glib.set("oh_resync", 1)

    # Success
    window.printLine(17, "Front-end biased!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
