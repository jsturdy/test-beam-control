# System imports
import time
from system import *

# Create window
window = Window("Acquire tracking data")

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
window.printBox(0, 9, 8, "BC:", "Default", "left")
window.printBox(0, 10, 8, "EC:", "Default", "left")
window.printBox(0, 11, 8, "ChipID:", "Default", "left")
window.printBox(0, 12, 8, "Data 1:", "Default", "left")
window.printBox(0, 13, 8, "Data 2:", "Default", "left")
window.printBox(0, 14, 8, "Data 3:", "Default", "left")
window.printBox(0, 15, 8, "Data 4:", "Default", "left")
window.printBox(0, 16, 8, "CRC:", "Default", "left")
window.printBox(0, 17, 8, "BX:", "Default", "left")

# File to save to
fileName = "../../test-beam-data/tracking/" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
f = open(fileName,"w")
f.write("Acquire tracking data\n")
f.write("Time: " + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n")
f.write("Run number: " + str(runNumber) + "\n")
f.write("BC;EC;ChipID;event;CRC;BX\n")

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

    event = bc + ";" + ec + ";" + chipid + ";" + data1 + data2 + data3 + data4 + ";" + crc + ";" + bx + "\n"
    f.write(event)

    window.printBox(8, 9, 10, bc, "Default", "left")
    window.printBox(8, 10, 10, ec, "Default", "left")
    window.printBox(8, 11, 10, chipid, "Default", "left")
    window.printBox(8, 12, 32, data1, "Default", "left")
    window.printBox(8, 13, 32, data2, "Default", "left")
    window.printBox(8, 14, 32, data3, "Default", "left")
    window.printBox(8, 15, 32, data4, "Default", "left")
    window.printBox(8, 16, 10, crc, "Default", "left")
    window.printBox(8, 17, 10, bx, "Default", "left")

    nEvents += 1

# Close window
window.close()
