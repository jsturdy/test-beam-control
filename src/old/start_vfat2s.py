# System imports
from system import *

# Create window
window = Window("Start VFAT2s")

# Get GLIB access
glib = GLIB('192.168.0.115', 'register_mapping.dat')
glib.setWindow(window)

# Print GLIB firmware version
glib_firmware_version = glib.get('glib_firmware_version')
window.printBox(0, 4, 40, "GLIB firmware version: ", "Default", "right")
window.printBox(40, 4, 40, hex(glib_firmware_version), "Default", "left")

# Print OptoHybrid firmware version
oh_firmware_version = glib.get('oh_firmware_version')
window.printBox(0, 5, 40, "OptoHybrid firmware version: ", "Default", "right")
window.printBox(40, 5, 40, hex(oh_firmware_version), "Default", "left")

# Design
window.printLine(7, "Select the VFAT2s you want to start (1 or 0)", "Info", "center")

# VFAT2s
window.printBox(0, 9, 40, "VFAT2 #8: ", "Default", "right")
window.printBox(0, 10, 40, "VFAT2 #9: ", "Default", "right")
window.printBox(0, 11, 40, "VFAT2 #10: ", "Default", "right")
window.printBox(0, 12, 40, "VFAT2 #11: ", "Default", "right")
window.printBox(0, 13, 40, "VFAT2 #12: ", "Default", "right")
window.printBox(0, 14, 40, "VFAT2 #13: ", "Default", "right")

# Get values
n8 = window.getInt(40, 9, 10)
n9 = window.getInt(40, 10, 10)
n10 = window.getInt(40, 11, 10)
n11 = window.getInt(40, 12, 10)
n12 = window.getInt(40, 13, 10)
n13 = window.getInt(40, 14, 10)

# Design
window.printLine(16, "Press [s] to start the VFAT2s or [ctrl+c] to quit", "Info", "center")

# Wait for Start signal
while(True):
    c = window.getChar()
    if (c == ord('s')):
        break

# Start the VFAT2
if (n8 == 1):
    glib.setVFAT2(8, 'ctrl0', 0x37)
if (n9 == 1):
    glib.setVFAT2(9, 'ctrl0', 0x37)
if (n10 == 1):
    glib.setVFAT2(10, 'ctrl0', 0x37)
if (n11 == 1):
    glib.setVFAT2(11, 'ctrl0', 0x37)
if (n12 == 1):
    glib.setVFAT2(12, 'ctrl0', 0x37)
if (n13 == 1):
    glib.setVFAT2(13, 'ctrl0', 0x37)

# Design
window.printLine(17, "VFAT2s started", "Success", "center")
window.printLine(18, "Press [q] to quit the program", "Warning", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
