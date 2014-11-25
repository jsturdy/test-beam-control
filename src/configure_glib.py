# System imports
from system import *

# Create window
window = Window("Configure the GLIB")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# GLIB version
glib_firmware_version = glib.get("glib_firmware_version")
window.printLine(4, "GLIB firmware version: " + hex(glib_firmware_version))

# SBit source
current = glib.get("glib_sbit_select") + 8
sbitSource = window.inputInt(6, "SBit VFAT2 select [8-13] ("+ str(current) + "):", 2, 8, 13, current)

# Design
window.printLine(8, "Press [s] to apply the settings.", "Info", "center")
window.waitForKey("s")

# Apply values
glib.set("glib_sbit_select", (sbitSource - 8))

# Log the changes
save = Save("log")
save.writeLine("GLIB configuration changed")
save.writePair("glib_sbit_select", (sbitSource - 8))
save.close()

# Design
window.printLine(9, "Settings applied!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
