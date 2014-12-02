# System imports
from kernel import *

# Create window
window = Window("Power VFAT2s On or Off")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Design
window.printLine(4, "Select the VFAT2s you want to Power On [1] or Off [0].", "Default", "left")

# Get current status
VFAT2 = [False, False, False, False, False, False]
VFAT2[0] = "" if (glib.getVFAT2(8, "ctrl0", True) & 0x1) else 0
VFAT2[1] = 1 if (glib.getVFAT2(9, "ctrl0", True) & 0x1) else 0
VFAT2[2] = 1 if (glib.getVFAT2(10, "ctrl0", True) & 0x1) else 0
VFAT2[3] = 1 if (glib.getVFAT2(11, "ctrl0", True) & 0x1) else 0
VFAT2[4] = 1 if (glib.getVFAT2(12, "ctrl0", True) & 0x1) else 0
VFAT2[5] = 1 if (glib.getVFAT2(13, "ctrl0", True) & 0x1) else 0

# VFAT2s
VFAT2[0] = window.inputInt(5, "VFAT2 #8  (" + ("On " if (VFAT2[0] == 1) else "Off") + "):", 1, 0, 1, VFAT2[0])
VFAT2[1] = window.inputInt(6, "VFAT2 #9  (" + ("On " if (VFAT2[1] == 1) else "Off") + "):", 1, 0, 1, VFAT2[1])
VFAT2[2] = window.inputInt(7, "VFAT2 #10 (" + ("On " if (VFAT2[2] == 1) else "Off") + "):", 1, 0, 1, VFAT2[2])
VFAT2[3] = window.inputInt(8, "VFAT2 #11 (" + ("On " if (VFAT2[3] == 1) else "Off") + "):", 1, 0, 1, VFAT2[3])
VFAT2[4] = window.inputInt(9, "VFAT2 #12 (" + ("On " if (VFAT2[4] == 1) else "Off") + "):", 1, 0, 1, VFAT2[4])
VFAT2[5] = window.inputInt(10, "VFAT2 #13 (" + ("On " if (VFAT2[5] == 1) else "Off") + "):", 1, 0, 1, VFAT2[5])

# Design
window.printLine(13, "Press [s] to apply the settings.", "Info", "center")
window.waitForKey("s")

#
for i in range(0, 6):
    if (glib.isVFAT2Present(i + 8) == True):
        config = glib.getVFAT2(i + 8, 'ctrl0')
        if (VFAT2[i] == 1):
            glib.setVFAT2(i + 8, 'ctrl0', 0x37)
        else:
            glib.setVFAT2(i + 8, 'ctrl0', 0x36)

# Send Resync signal
glib.set("oh_resync", 0x1)

# Log the changes
save = Save("log")
save.writeLine("VFAT2s turned On or Off")
save.writePair("VFAT2 #8", ("On" if (VFAT2[0] == 1) else "Off"))
save.writePair("VFAT2 #9", ("On" if (VFAT2[1] == 1) else "Off"))
save.writePair("VFAT2 #10", ("On" if (VFAT2[2] == 1) else "Off"))
save.writePair("VFAT2 #11", ("On" if (VFAT2[3] == 1) else "Off"))
save.writePair("VFAT2 #12", ("On" if (VFAT2[4] == 1) else "Off"))
save.writePair("VFAT2 #13", ("On" if (VFAT2[5] == 1) else "Off"))
save.close()

# Design
window.printLine(14, "Settings applied!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
