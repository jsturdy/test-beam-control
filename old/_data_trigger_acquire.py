# System imports
import time
from kernel import *

# Create window
window = Window("Acquire trigger data")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Get run number
runNumber = window.inputInt(4, "Run number [0-99999]:", 5, 0, 99999, 0)

# Design
window.printLine(6, "Press [s] to start the data taking and [ctrl+c] to quit.", "Info", "center")
window.waitForKey("s")

window.printLine(7, "Preparing acquisition...", "Info", "center")

# Save VFAT2"s parameters
vfat2Parameters = [None] * 6
vfat2Parameters[0] = glib.saveVFAT2(8)
vfat2Parameters[1] = glib.saveVFAT2(9)
vfat2Parameters[2] = glib.saveVFAT2(10)
vfat2Parameters[3] = glib.saveVFAT2(11)
vfat2Parameters[4] = glib.saveVFAT2(12)
vfat2Parameters[5] = glib.saveVFAT2(13)

# Open the save file
save = Save("trigger")
save.writePair("Run number", runNumber)
save.writeLine("-----")
save.writeDict(vfat2Parameters[0])
save.writeLine("-----")
save.writeDict(vfat2Parameters[1])
save.writeLine("-----")
save.writeDict(vfat2Parameters[2])
save.writeLine("-----")
save.writeDict(vfat2Parameters[3])
save.writeLine("-----")
save.writeDict(vfat2Parameters[4])
save.writeLine("-----")
save.writeDict(vfat2Parameters[5])
save.writeLine("-----")

# Design
window.printBox(0, 9, 7, "BX:")
window.printBox(0, 10, 7, "SBits:")

# Events
nEvents = 0

# Strips
strips = [0] * 6

# Get data
while(True):

    window.printLine(7, str(nEvents) + " saved!", "Info", "center")

    time.sleep(0.01)

    # Get data
    packet1 = glib.get("glib_request_trigger_data")

    # Format data
    bx = hex((0xffffffc0 & packet1) >> 6)
    sbits = bin(0x0000003f & packet1)[2:].zfill(6)

    # Save data
    event = bx + ";" + sbits
    save.writeLine(event)

    # Print data
    window.printBox(7, 9, 10, bx)
    window.printBox(7, 10, 7, sbits)

    # Histogram
    for i in range(0, 6):
        strips[i] += (1 if (sbits[i] == "1") else 0)

    graph1D(strips, 0, 5)

    # Next event
    nEvents += 1

# Close window
window.close()
