# System imports
import time
from system import *

# Create window
window = Window("Observer trigger data")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Empty trigger data
glib.set("glib_empty_trigger_data", 0)

# Design
window.printLine(4, "Press [s] to get a new data packet.", "Info", "center")

# Design
window.printBox(0, 6, 7, "BX:", "Default", "left")
window.printBox(0, 7, 7, "SBits:", "Default", "left")

# Get data
while(True):

    window.printBox(7, 6, 10, "", "Default", "left")
    window.printBox(7, 7, 7, "", "Default", "left")

    time.sleep(0.1)

    packet1 = glib.get("glib_request_trigger_data")

    bx = hex((0xffffffc0 & packet1) >> 6)
    sbits = bin(0x0000003f & packet1)[2:].zfill(6)

    window.printBox(7, 6, 10, bx, "Default", "left")
    window.printBox(7, 7, 7, sbits, "Default", "left")

    # Wait for Start signal
    window.waitForKey("s")

# Close window
window.close()
