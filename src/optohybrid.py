# System imports
from system import *

# Create window
window = Window("Configure the OptoHybrid")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# OptoHybrid version
oh_firmware_version = glib.get("oh_firmware_version")
window.printLine(4, "OptoHybrid firmware version: " + hex(oh_firmware_version), "Default", "left")

# Trigger source
current = glib.get("oh_trigger_source")
window.printBox(0, 6, 26, "Trigger source [0-2] (" + str(current) + "):", "Default", "left")
window.printBox(0, 7, 20, "0: internal", "Default", "left")
window.printBox(20, 7, 20, "1: external", "Default", "left")
window.printBox(40, 7, 20, "2: both", "Default", "left")
inputData = window.getInt(26, 6, 1)
triggerSource = current if (inputData < 0 or inputData > 2) else inputData
window.printBox(26, 6, 1, str(triggerSource), "Input", "left")

# SBit source
current = glib.get("oh_sbit_select") + 8
window.printBox(0, 9, 30, "SBit VFAT2 select [8-13] ("+ str(current) + "):", "Default", "left")
inputData = window.getInt(30, 9, 2)
sbitSource = 8 if (inputData < 8 or inputData > 13) else inputData
window.printBox(30, 9, 2, str(sbitSource), "Input", "left")

# VFAT2 clock source
current = glib.get("oh_vfat2_src_select")
window.printBox(0, 11, 30, "VFAT2 clock source [0-1] ("+ str(current) + "):", "Default", "left")
window.printBox(0, 12, 20, "0: internal", "Default", "left")
window.printBox(20, 12, 20, "1: external", "Default", "left")
inputData = window.getInt(30, 11, 2)
vfat2Source = current if (inputData < 0 or inputData > 1) else inputData
window.printBox(30, 11, 1, str(vfat2Source), "Input", "left")

# VFAT2 fallback
current = glib.get("oh_vfat2_fallback")
window.printBox(0, 14, 38, "VFAT2 allow clock fallback [0-1] ("+ str(current) + "):", "Default", "left")
inputData = window.getInt(38, 14, 1)
vfat2Fallback = current if (inputData < 0 or inputData > 1) else inputData
window.printBox(38, 14, 1, str(vfat2Fallback), "Input", "left")

# CDCE clock source
current = glib.get("oh_cdce_src_select")
window.printBox(0, 16, 29, "CDCE clock source [0-1] ("+ str(current) + "):", "Default", "left")
window.printBox(0, 17, 20, "0: internal", "Default", "left")
window.printBox(20, 17, 20, "1: external", "Default", "left")
inputData = window.getInt(29, 16, 2)
cdceSource = current if (inputData < 0 or inputData > 1) else inputData
window.printBox(29, 16, 1, str(cdceSource), "Input", "left")

# CDCE clock source
current = glib.get("oh_cdce_fallback")
window.printBox(0, 19, 37, "CDCE allow clock fallback [0-1] ("+ str(current) + "):", "Default", "left")
inputData = window.getInt(37, 19, 1)
cdceFallback = current if (inputData < 0 or inputData > 1) else inputData
window.printBox(37, 19, 1, str(cdceFallback), "Input", "left")

# Design
window.printLine(21, "Press [s] to apply the settings.", "Info", "center")
window.waitForKey("s")

# Apply values
glib.set("oh_trigger_source", triggerSource)
glib.set("oh_sbit_select", (sbitSource - 8))
glib.set("oh_vfat2_src_select", vfat2Source)
glib.set("oh_vfat2_fallback", vfat2Fallback)
glib.set("oh_cdce_src_select", cdceSource)
glib.set("oh_cdce_fallback", cdceFallback)

# Design
window.printLine(22, "Settings applied!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
