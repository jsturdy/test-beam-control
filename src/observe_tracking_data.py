# System imports
import time
from system import *

# Create window
window = Window("Observer tracking data")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Design
window.printLine(4, "Press [s] to get a new data packet or [ctrl+c] to quit", "Info", "center")

# Design
window.printBox(0, 6, 8, "BC:")
window.printBox(0, 7, 8, "EC:")
window.printBox(0, 8, 8, "ChipID:")
window.printBox(0, 9, 8, "Data 1:")
window.printBox(0, 10, 8, "Data 2:")
window.printBox(0, 11, 8, "Data 3:")
window.printBox(0, 12, 8, "Data 4:")
window.printBox(0, 13, 8, "CRC:")
window.printBox(0, 14, 8, "BX:")

# Get data
while(True):

    window.printBox(8, 6, 10, "")
    window.printBox(8, 7, 10, "")
    window.printBox(8, 8, 10, "")
    window.printBox(8, 9, 32, "")
    window.printBox(8, 10, 32, "")
    window.printBox(8, 11, 32, "")
    window.printBox(8, 12, 32, "")
    window.printBox(8, 13, 10, "")
    window.printBox(8, 14, 10, "")

    time.sleep(0.1)

    # Get a tracking packet (with a limit)
    while (True):

        # Request new data
        isNewData = glib.get("glib_request_tracking_data")
        time.sleep(0.1)

        if (isNewData == 0x1):
            break

    packet1 = glib.get("glib_tracking_data_1")
    packet2 = glib.get("glib_tracking_data_2")
    packet3 = glib.get("glib_tracking_data_3")
    packet4 = glib.get("glib_tracking_data_4")
    packet5 = glib.get("glib_tracking_data_5")
    packet6 = glib.get("glib_tracking_data_6")
    packet7 = glib.get("glib_tracking_data_7")

    bc = hex((0x0fff0000 & packet6) >> 16)
    ec = hex((0x00000ff0 & packet6) >> 4)
    chipid = hex((0x0fff0000 & packet5) >> 16)
    data1 = bin(((0x0000ffff & packet5) << 16) | ((0xffff0000 & packet4) >> 16))[2:].zfill(32)
    data2 = bin(((0x0000ffff & packet4) << 16) | ((0xffff0000 & packet3) >> 16))[2:].zfill(32)
    data3 = bin(((0x0000ffff & packet3) << 16) | ((0xffff0000 & packet2) >> 16))[2:].zfill(32)
    data4 = bin(((0x0000ffff & packet2) << 16) | ((0xffff0000 & packet1) >> 16))[2:].zfill(32)
    crc = hex(0x0000ffff & packet1)
    bx = hex(packet7)

    window.printBox(8, 6, 10, bc)
    window.printBox(8, 7, 10, ec)
    window.printBox(8, 8, 10, chipid)
    window.printBox(8, 9, 32, data1)
    window.printBox(8, 10, 32, data2)
    window.printBox(8, 11, 32, data3)
    window.printBox(8, 12, 32, data4)
    window.printBox(8, 13, 10, crc)
    window.printBox(8, 14, 10, bx)

    # Wait for Start signal
    window.waitForKey("s")

# Close window
window.close()
