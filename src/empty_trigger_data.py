# System imports
import sys, os
from system import *

# Create window
window = Window("Empty trigger data")

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
window.printLine(7, "Press [s] to empty the trigger data or [ctrl+c] to quit", "Info", "center")

# Wait for Start signal
while(True):
    c = window.getChar()
    if (c == ord('s')):
        break

# Empty the buffers
glib.set('glib_empty_trigger_data', 0)

# Design
window.printLine(8, "Trigger buffers emptied", "Success", "center")
window.printLine(9, "Press [q] to quit the program", "Warning", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
