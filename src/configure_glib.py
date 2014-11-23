# System imports
from system import *

# Create window
window = Window("Configure the GLIB")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# GLIB version
glib_firmware_version = glib.get("glib_firmware_version")
window.printLine(4, "GLIB firmware version: " + hex(glib_firmware_version), "Default", "left")

# SBit source
current = glib.get("glib_sbit_select") + 8
window.printBox(0, 6, 30, "SBit VFAT2 select [8-13] ("+ str(current) + "):", "Default", "left")
inputData = window.getInt(30, 6, 2)
sbitSource = current if (inputData < 8 or inputData > 13) else inputData
window.printBox(30, 6, 2, str(sbitSource), "Input", "left")

# Design
window.printLine(8, "Press [s] to apply the settings.", "Info", "center")
window.waitForKey("s")

# Apply values
glib.set("glib_sbit_select", (sbitSource - 8))

# Design
window.printLine(9, "Settings applied!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
