# System imports
from system import *

# Create window
window = Window("Power VFAT2s On or Off")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Design
window.printLine(4, "Select the VFAT2s you want to Power On [1] or Off [0].", "Default", "left")

# Get current status
VFAT2 = [False, False, False, False, False, False]
VFAT2[0] = 1 if (glib.getVFAT2(8, "ctrl0", True) & 0x1) else 0
VFAT2[1] = 1 if (glib.getVFAT2(9, "ctrl0", True) & 0x1) else 0
VFAT2[2] = 1 if (glib.getVFAT2(10, "ctrl0", True) & 0x1) else 0
VFAT2[3] = 1 if (glib.getVFAT2(11, "ctrl0", True) & 0x1) else 0
VFAT2[4] = 1 if (glib.getVFAT2(12, "ctrl0", True) & 0x1) else 0
VFAT2[5] = 1 if (glib.getVFAT2(13, "ctrl0", True) & 0x1) else 0

# VFAT2s
window.printBox(0, 5, 17, "VFAT2 #8  [" + ("On" if (VFAT2[0] == 1) else "Off") + "]: ", "Default", "left")
inputData = window.getInt(17, 5, 1)
VFAT2[0] = VFAT2[0] if (inputData == -1) else inputData
window.printBox(17, 5, 3, ("On" if VFAT2[0] else "Off"), "Input", "left")

window.printBox(0, 6, 17, "VFAT2 #9  [" + ("On" if (VFAT2[1] == 1) else "Off") + "]: ", "Default", "left")
inputData = window.getInt(17, 6, 1)
VFAT2[1] = VFAT2[1] if (inputData == -1) else inputData
window.printBox(17, 6, 3, ("On" if VFAT2[1] else "Off"), "Input", "left")

window.printBox(0, 7, 17, "VFAT2 #10 [" + ("On" if (VFAT2[2] == 1) else "Off") + "]: ", "Default", "left")
inputData = window.getInt(17, 7, 1)
VFAT2[2] = VFAT2[2] if (inputData == -1) else inputData
window.printBox(17, 7, 3, ("On" if VFAT2[2] else "Off"), "Input", "left")

window.printBox(0, 8, 17, "VFAT2 #11 [" + ("On" if (VFAT2[3] == 1) else "Off") + "]: ", "Default", "left")
inputData = window.getInt(17, 8, 1)
VFAT2[3] = VFAT2[3] if (inputData == -1) else inputData
window.printBox(17, 8, 3, ("On" if VFAT2[3] else "Off"), "Input", "left")

window.printBox(0, 9, 17, "VFAT2 #12 [" + ("On" if (VFAT2[4] == 1) else "Off") + "]: ", "Default", "left")
inputData = window.getInt(17, 9, 1)
VFAT2[4] = VFAT2[4] if (inputData == -1) else inputData
window.printBox(17, 9, 3, ("On" if VFAT2[4] else "Off"), "Input", "left")

window.printBox(0, 10, 17, "VFAT2 #13 [" + ("On" if (VFAT2[5] == 1) else "Off") + "]: ", "Default", "left")
inputData = window.getInt(17, 10, 1)
VFAT2[5] = VFAT2[5] if (inputData == -1) else inputData
window.printBox(17, 10, 3, ("On" if VFAT2[5] else "Off"), "Input", "left")

# Design
window.printLine(13, "Press [s] to apply the settings.", "Info", "center")
window.waitForKey("s")

#
for i in range(0, 6):
    if (glib.isVFAT2(i + 8) == 1):
        config = glib.getVFAT2(i + 8, 'ctrl0')
        if (VFAT2[i] == 1):
            glib.setVFAT2(i + 8, 'ctrl0', 0x37)
        else:
            glib.setVFAT2(i + 8, 'ctrl0', 0x36)

# Send Resync signal
glib.set("oh_resync", 0x1)

# Design
window.printLine(14, "Settings applied!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
