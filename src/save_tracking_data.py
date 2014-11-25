# System imports
import time
from system import *

# Create window
window = Window("Acquire tracking data")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Get run number
runNumber = window.inputInt(4, "Run number:", 10, 0, 500000, 0)

# Design
window.printLine(6, "Press [s] to start the data taking and [ctrl+c] to quit.", "Info", "center")
window.waitForKey("s")

# Design
window.printBox(0, 9, 8, "BC:")
window.printBox(0, 10, 8, "EC:")
window.printBox(0, 11, 8, "ChipID:")
window.printBox(0, 12, 8, "Data 1:")
window.printBox(0, 13, 8, "Data 2:")
window.printBox(0, 14, 8, "Data 3:")
window.printBox(0, 15, 8, "Data 4:")
window.printBox(0, 16, 8, "CRC:")
window.printBox(0, 17, 8, "BX:")

# Save VFAT2's parameters
vfat2Parameters = [None] * 6
vfat2Parameters[0] = glib.saveVFAT2(8)
vfat2Parameters[1] = glib.saveVFAT2(9)
vfat2Parameters[2] = glib.saveVFAT2(10)
vfat2Parameters[3] = glib.saveVFAT2(11)
vfat2Parameters[4] = glib.saveVFAT2(12)
vfat2Parameters[5] = glib.saveVFAT2(13)

# Open the save file
save = Save("tracking")
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

# Events
nEvents = 0

# Get data
while(True):

    window.printLine(7, str(nEvents) + " saved!", "Info", "center")

    # Get a tracking packet (with a limit)
    while (True):

        # Request new data
        isNewData = glib.get("glib_request_tracking_data")
        time.sleep(0.01)

        if (isNewData == 0x1):
            break

    packet1 = glib.get("glib_tracking_data_1")
    packet2 = glib.get("glib_tracking_data_2")
    packet3 = glib.get("glib_tracking_data_3")
    packet4 = glib.get("glib_tracking_data_4")
    packet5 = glib.get("glib_tracking_data_5")
    packet6 = glib.get("glib_tracking_data_6")
    packet7 = glib.get("glib_tracking_data_7")

    bc = str((0x0fff0000 & packet6) >> 16)
    ec = str((0x00000ff0 & packet6) >> 4)
    chipid = str((0x0fff0000 & packet5) >> 16)
    data1 = bin(((0x0000ffff & packet5) << 16) | ((0xffff0000 & packet4) >> 16))[2:].zfill(32)
    data2 = bin(((0x0000ffff & packet4) << 16) | ((0xffff0000 & packet3) >> 16))[2:].zfill(32)
    data3 = bin(((0x0000ffff & packet3) << 16) | ((0xffff0000 & packet2) >> 16))[2:].zfill(32)
    data4 = bin(((0x0000ffff & packet2) << 16) | ((0xffff0000 & packet1) >> 16))[2:].zfill(32)
    crc = str(0x0000ffff & packet1)
    bx = str(packet7)

    event = bc + ";" + ec + ";" + chipid + ";" + data1 + data2 + data3 + data4 + ";" + crc + ";" + bx
    save.writeLine(event)

    window.printBox(8, 9, 10, bc)
    window.printBox(8, 10, 10, ec)
    window.printBox(8, 11, 10, chipid)
    window.printBox(8, 12, 32, data1)
    window.printBox(8, 13, 32, data2)
    window.printBox(8, 14, 32, data3)
    window.printBox(8, 15, 32, data4)
    window.printBox(8, 16, 10, crc)
    window.printBox(8, 17, 10, bx)

    nEvents += 1

# Close window
window.close()
