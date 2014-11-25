# System imports
from kernel import *

# Create window
window = Window("Configure the system")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# GLIB version
glib_firmware_version = glib.get("glib_firmware_version")
window.printLine(4, "GLIB firmware version: " + hex(glib_firmware_version))

# OptoHybrid version
oh_firmware_version = glib.get("oh_firmware_version")
window.printLine(6, "OptoHybrid firmware version: " + hex(oh_firmware_version))

# Trigger source
current = glib.get("oh_trigger_source")
window.printBox(0, 9, 20, "0: internal")
window.printBox(20, 9, 20, "1: external")
window.printBox(40, 9, 20, "2: both")
triggerSource = window.inputInt(8, "Trigger source [0-2] ("+ str(current) + "):", 1, 0, 2, current)

# SBit source
current = glib.get("oh_sbit_select") + 8
sbitSource = window.inputInt(11, "SBit VFAT2 select [8-13] ("+ str(current) + "):", 2, 8, 13, current)

# VFAT2 clock source
current = glib.get("oh_vfat2_src_select")
window.printBox(0, 14, 20, "0: internal")
window.printBox(20, 14, 20, "1: external")
vfat2Source = window.inputInt(13, "VFAT2 clock source [0-1] ("+ str(current) + "):", 1, 0, 1, current)

# VFAT2 fallback
current = glib.get("oh_vfat2_fallback")
vfat2Fallback = window.inputInt(16, "VFAT2 allow clock fallback [0-1] ("+ str(current) + "):", 1, 0, 1, current)

# CDCE clock source
current = glib.get("oh_cdce_src_select")
window.printBox(0, 19, 20, "0: internal")
window.printBox(20, 19, 20, "1: external")
cdceSource = window.inputInt(18, "CDCE clock source [0-1] ("+ str(current) + "):", 1, 0, 1, current)

# CDCE clock source
current = glib.get("oh_cdce_fallback")
cdceFallback = window.inputInt(21, "CDCE allow clock fallback [0-1] ("+ str(current) + "):", 1, 0, 1, current)

# Design
window.printLine(23, "Press [s] to apply the settings.", "Info", "center")
window.waitForKey("s")

# Apply values
glib.set("oh_vfat2_fallback", vfat2Fallback)
glib.set("oh_cdce_fallback", cdceFallback)
glib.set("oh_trigger_source", triggerSource)
glib.set("glib_sbit_select", (sbitSource - 8))
glib.set("oh_sbit_select", (sbitSource - 8))
glib.set("oh_vfat2_src_select", vfat2Source)
glib.set("oh_cdce_src_select", cdceSource)

# Log the changes
save = Save("log")
save.writeLine("System configuration changed")
save.writePair("oh_trigger_source", triggerSource)
save.writePair("glib_sbit_select", (sbitSource - 8))
save.writePair("oh_sbit_select", (sbitSource - 8))
save.writePair("oh_vfat2_src_select", vfat2Source)
save.writePair("oh_vfat2_fallback", vfat2Fallback)
save.writePair("oh_cdce_src_select", cdceSource)
save.writePair("oh_cdce_fallback", cdceFallback)
save.close()

# Design
window.printLine(24, "Settings applied!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
