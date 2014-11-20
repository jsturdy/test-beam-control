# System imports
import time
from system import *

# Create window
window = Window("Observer trigger data")

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

# Empty trigger data
glib.set("glib_empty_trigger_data", 0)

# Design
window.printLine(7, "Press [s] to get a new data packet or [ctrl+c] to quit", "Info", "center")

# Wait for Start signal
while(True):
    c = window.getChar()
    if (c == ord('s')):
        break

# Design
window.printBox(0, 9, 40, "BX: ", "Default", "right")
window.printBox(0, 10, 40, "SBits: ", "Default", "right")

# Get data
while(True):

    window.printBox(40, 9, 40, "", "Default", "left")
    window.printBox(40, 10, 40, "", "Default", "left")

    # Get a tracking packet (with a limit)
    while (True):

        # Request new data
        isNewData = glib.get("glib_request_tracking_data")
        time.sleep(0.1)

        if (isNewData == 0x1):
            break

    packet1 = glib.get("glib_request_trigger_data")

    bx = hex((0xffffffc0 & packet1) >> 6)
    sbits = bin(0x0000003f & packet1)

    window.printBox(40, 9, 40, bx, "Default", "left")
    window.printBox(40, 10, 40, sbits, "Default", "left")

    # Wait for Start signal
    while(True):
        c = window.getChar()
        if (c == ord('s')):
            break

    time.sleep(0.1)

# Close window
window.close()
