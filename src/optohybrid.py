# System imports
from system import *

# Create window
window = Window("Configure the OptoHybrid")

# Get GLIB access
glib = GLIB("192.168.0.115", "register_mapping.dat")
glib.setWindow(window)

# Trigger source
window.printBox(0, 4, 20, "Trigger source [0]:", "Default", "left")
window.printBox(0, 5, 20, "0: internal", "Default", "left")
window.printBox(20, 5, 20, "1: external", "Default", "left")
window.printBox(40, 5, 20, "2: both", "Default", "left")
inputData = window.getInt(20, 4, 1)
triggerSource = 0 if (inputData < 0 or inputData > 2) else inputData
window.printBox(20, 4, 1, str(triggerSource), "Input", "left")

# SBit source
window.printBox(0, 7, 26, "SBit VFAT2 select [8-13]:", "Default", "left")
inputData = window.getInt(26, 7, 2)
sbitSource = 8 if (inputData < 8 or inputData > 13) else inputData
window.printBox(26, 7, 2, str(sbitSource), "Input", "left")

# VFAT2 clock source
window.printBox(0, 9, 24, "VFAT2 clock source [0]:", "Default", "left")
window.printBox(0, 10, 20, "0: internal", "Default", "left")
window.printBox(20, 10, 20, "1: external", "Default", "left")
inputData = window.getInt(24, 9, 2)
vfat2Source = 0 if (inputData < 0 or inputData > 1) else inputData
window.printBox(24, 9, 1, str(vfat2Source), "Input", "left")

# VFAT2 fallback
window.printBox(0, 12, 32, "VFAT2 allow clock fallback [1]:", "Default", "left")
inputData = window.getInt(32, 12, 1)
vfat2Fallback = 1 if (inputData < 0 or inputData > 1) else inputData
window.printBox(32, 12, 1, str(vfat2Fallback), "Input", "left")

# CDCE clock source
window.printBox(0, 14, 23, "CDCE clock source [0]:", "Default", "left")
window.printBox(0, 15, 20, "0: internal", "Default", "left")
window.printBox(20, 15, 20, "1: external", "Default", "left")
inputData = window.getInt(23, 14, 2)
cdceSource = 0 if (inputData < 0 or inputData > 1) else inputData
window.printBox(23, 14, 1, str(cdceSource), "Input", "left")

# CDCE clock source
window.printBox(0, 17, 31, "CDCE allow clock fallback [1]:", "Default", "left")
inputData = window.getInt(31, 17, 1)
cdceFallback = 1 if (inputData < 0 or inputData > 1) else inputData
window.printBox(31, 17, 1, str(cdceFallback), "Input", "left")

# Design
window.printLine(19, "Press [s] to apply the settings.", "Info", "center")
window.waitForKey("s")

# Apply values
glib.set("oh_trigger_source", triggerSource)
glib.set("oh_sbit_select", sbitSource)
glib.set("oh_vfat2_src_select", vfat2Source)
glib.set("oh_vfat2_fallback", vfat2Fallback)
glib.set("oh_cdce_src_select", cdceSource)
glib.set("oh_cdce_fallback", cdceFallback)

# Design
window.printLine(20, "Settings applied!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
