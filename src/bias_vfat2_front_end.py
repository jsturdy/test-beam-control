# System imports
from system import *

# Create window
window = Window("Bias a VFAT2's front-end")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Get a VFAT2 number
vfat2ID = window.inputInt(4, "Select a VFAT2 to scan [8-13]:", 2, 8, 13, 8)

# Test if VFAT2 is present
if (glib.isVFAT2(vfat2ID) == False):
    # Error
    window.printLine(6, "The selected VFAT2 is not present!", "Error", "center")

else:

    # Description
    window.printLine(6, "Register    [Range] [Recommended] (Current)")

    # Get a IPreampIn
    current = glib.getVFAT2(vfat2ID, "ipreampin")
    IPreampIn = window.inputInt(7, "IPreampIn   [0-255] [168] (" + str(current) + "):", 3, 0, 255, current)

    # Get a IPreampFeed
    current = glib.getVFAT2(vfat2ID, "ipreampfeed")
    IPreampFeed = window.inputInt(8, "IPreampFeed [0-255] [80]  (" + str(current) + "):", 3, 0, 255, current)

    # Get a IPreampOut
    current = glib.getVFAT2(vfat2ID, "ipreampout")
    IPreampOut = window.inputInt(9, "IPreampOut  [0-255] [150] (" + str(current) + "):", 3, 0, 255, current)

    # Get a IShaper
    current = glib.getVFAT2(vfat2ID, "ishaper")
    IShaper = window.inputInt(10, "IShaper     [0-255] [150] (" + str(current) + "):", 3, 0, 255, current)

    # Get a IShaperFeed
    current = glib.getVFAT2(vfat2ID, "ishaperfeed")
    IShaperFeed = window.inputInt(11, "IShaperFeed [0-255] [100] (" + str(current) + "):", 3, 0, 255, current)

    # Get a IComp
    current = glib.getVFAT2(vfat2ID, "icomp")
    IComp = window.inputInt(12, "IComp       [0-255] [120] (" + str(current) + "):", 3, 0, 255, current)

    # Get a VThreshold1
    current = glib.getVFAT2(vfat2ID, "vthreshold1")
    VThreshold1 = window.inputInt(13, "VThreshold1 [0-255] [10]  (" + str(current) + "):", 3, 0, 255, current)

    # Get a VThreshold2
    current = glib.getVFAT2(vfat2ID, "vthreshold2")
    VThreshold2 = window.inputInt(14, "VThreshold2 [0-255] [0]   (" + str(current) + "):", 3, 0, 255, current)

    #
    window.printLine(16, "Press [s] to bias the front-end.", "Info", "center")
    window.waitForKey("s")

    # Bias front-end
    glib.setVFAT2(vfat2ID, "ipreampin", IPreampIn)
    glib.setVFAT2(vfat2ID, "ipreampfeed", IPreampFeed)
    glib.setVFAT2(vfat2ID, "ipreampout", IPreampOut)
    glib.setVFAT2(vfat2ID, "ishaper", IShaper)
    glib.setVFAT2(vfat2ID, "ishaperfeed", IShaperFeed)
    glib.setVFAT2(vfat2ID, "icomp", IComp)
    glib.setVFAT2(vfat2ID, "vthreshold1", VThreshold1)
    glib.setVFAT2(vfat2ID, "vthreshold2", VThreshold2)
    glib.set("oh_resync", 1)

    # Log the changes
    save = Save("log")
    save.writeLine("VFAT2 front end-biased")
    save.writePair("ipreampin", IPreampIn)
    save.writePair("ipreampfeed", IPreampFeed)
    save.writePair("ipreampout", IPreampOut)
    save.writePair("ishaper", IShaper)
    save.writePair("ishaperfeed", IShaperFeed)
    save.writePair("icomp", IComp)
    save.writePair("vthreshold1", VThreshold1)
    save.writePair("vthreshold2", VThreshold2)
    save.close()

    # Success
    window.printLine(17, "Front-end biased!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
