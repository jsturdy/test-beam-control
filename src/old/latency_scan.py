# System imports
import time
from system import *

# Create window
window = Window("Latency scan")

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
window.printLine(7, "Latency scan", "Info", "center")

# VFAT2 select
window.printBox(0, 9, 40, "VFAT2 to scan: ", "Default", "right")
window.printBox(50, 9, 10, "[8]", "Default", "left")

window.printBox(0, 10, 40, "Threshold: ", "Default", "right")
window.printBox(50, 10, 10, "[60]", "Default", "left")

window.printBox(0, 11, 40, "Minimum latency: ", "Default", "right")
window.printBox(50, 11, 10, "[0]", "Default", "left")

window.printBox(0, 12, 40, "Maximum latency: ", "Default", "right")
window.printBox(50, 12, 10, "[255]", "Default", "left")

window.printBox(0, 13, 40, "# of events per threshold: ", "Default", "right")
window.printBox(50, 13, 10, "[100]", "Default", "left")

# Ask values
VFAT2 = window.getInt(40, 9, 10)
threshold = window.getInt(40, 10, 10)
tmin = window.getInt(40, 11, 10)
tmax = window.getInt(40, 12, 10)
nevents = window.getInt(40, 13, 10)

if (VFAT2 == -1):
    VFAT2 = 8
if (threshold == -1):
    threshold = 60
if (tmin == -1):
    tmin = 0
if (tmax == -1):
    tmax = 255
if (nevents == -1):
    nevents = 100

# Design
window.printLine(15, "Press [s] to start scanning the latency", "Success", "center")

# Wait for Start signal
while(True):
    c = window.getChar()
    if (c == ord('s')):
        break

# Test if VFAT2 is present
testVFAT2Present = glib.getVFAT2(VFAT2, 'chipid0')

if (((testVFAT2Present & 0x4000000) >> 26) == 1):
    # Error
    window.printLine(20, "VFAT2 not present!", "Error", "center")

else:
    # Design
    window.printBox(0, 17, 40, "Latency: ", "Default", "right")
    window.printBox(0, 18, 40, "Percentage: ", "Default", "right")

    # Create a plot and its data
    latencies = []
    dataPoints = []

    # Set VFAT2 parameters
    ctrl2Old = glib.getVFAT2(VFAT2, 'ctrl2')
    glib.setVFAT2(VFAT2, 'ctrl2', ctrl2Old | 0x70)
    glib.setVFAT2(VFAT2, 'vthreshold1', threshold)
    glib.setVFAT2(VFAT2, 'vcal', 0xff)
    channel8Old = glib.getVFAT2(VFAT2, 'channel8')
    glib.setVFAT2(VFAT2, 'channel8', channel8Old | 0x40)

    # Loop over Threshold 1
    for latency in range(tmin, tmax + 1):

        # Design
        window.printBox(40, 17, 40, str(latency), "Default", "left")

        # Set Threshold 1
        glib.setVFAT2(VFAT2, 'latency', latency)

        # Send Resync signal
        glib.set('oh_resync', 0x1)

        # Empty tracking fifo
        glib.set('glib_empty_tracking_data', 0)

        # Efficiency variable
        hitCount = 0.

        # Read tracking packets
        for i in range(0, nevents):

            # Design
            percentage = (latency * nevents + i) / (nevents * (tmax - tmin) * 1.) * 100.
            window.printBox(40, 18, 40, str(percentage)[:5] + "%", "Default", "left")

            # Send 5 delayed signal (to be sure...)
            glib.set('oh_lv1a_and_calpulse', 40)
            glib.set('oh_lv1a_and_calpulse', 40)
            glib.set('oh_lv1a_and_calpulse', 40)
            glib.set('oh_lv1a_and_calpulse', 40)
            glib.set('oh_lv1a_and_calpulse', 40)

            # Get a tracking packet (with a limit)
            while (True):

                # Request new data
                isNewData = glib.get("glib_request_tracking_data")

                if (isNewData == 0x1):
                    break

            packet1 = glib.get("glib_tracking_data_1")
            packet2 = glib.get("glib_tracking_data_2")
            packet3 = glib.get("glib_tracking_data_3")
            packet4 = glib.get("glib_tracking_data_4")
            packet5 = glib.get("glib_tracking_data_5")

            data1 = ((0x0000ffff & packet5) << 16) | ((0xffff0000 & packet4) >> 16)
            data2 = ((0x0000ffff & packet4) << 16) | ((0xffff0000 & packet3) >> 16)
            data3 = ((0x0000ffff & packet3) << 16) | ((0xffff0000 & packet2) >> 16)
            data4 = ((0x0000ffff & packet2) << 16) | ((0xffff0000 & packet1) >> 16)

            if (data1 + data2 + data3 + data4 != 0):
                hitCount += 1.

        # Add data
        latencies.append(latency)
        dataPoints.append(hitCount / nevents)

        # Update plot
        graph(latencies, dataPoints, 0, 255, 0, 1)

        # Wait a bit
        time.sleep(0.1)

    # Restore old parameters
    glib.setVFAT2(VFAT2, 'ctrl2', ctrl2Old)
    glib.setVFAT2(VFAT2, 'channel8', channel8Old)

    # Success
    window.printLine(20, "Scan finished!", "Success", "center")

# Design
window.printLine(21, "Press [q] to quit the program", "Warning", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
