# System imports
import time
from system import *

# Create window
window = Window("Acquire trigger data")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Get run number
window.printBox(0, 4, 12, "Run number:", "Default", "left")
runNumber = window.getInt(12, 4, 10)
window.printBox(12, 4, 10, str(runNumber), "Input", "left")

# Design
window.printLine(6, "Press [s] to start the data taking and [ctrl+c] to quit.", "Info", "center")
window.waitForKey("s")

# Design
window.printBox(0, 9, 7, "BX:", "Default", "left")
window.printBox(0, 10, 7, "SBits:", "Default", "left")

# File to save to
fileName = "../data/trigger/" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
f = open(fileName,"w")
f.write("Trigger data tacking\n")
f.write("Time: " + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n")
f.write("Run number: " + str(runNumber) + "\n")
f.write("BX;event\n")

# Events
nEvents = 0

# Get data
while(True):

    window.printLine(7, str(nEvents) + " saved!", "Info", "center")

    time.sleep(0.01)

    # Get data
    packet1 = glib.get("glib_request_trigger_data")

    bx = hex((0xffffffc0 & packet1) >> 6)
    sbits = bin(0x0000003f & packet1)[2:].zfill(6)

    event = bx + ";" + sbits
    f.write(event)

    window.printBox(7, 9, 10, bx, "Default", "left")
    window.printBox(7, 10, 7, sbits, "Default", "left")

    nEvents += 1

# Close window
window.close()
