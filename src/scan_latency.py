# System imports
import time
from system import *

# Create window
window = Window("Latency scan")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Warning
window.printLine(4, "For this scan to work, the VFAT2 has to be biased and running!", "Warning", "center")

# Get a VFAT2 number
window.printBox(0, 6, 30, "Select a VFAT2 to scan [8-13]:", "Default", "left")
inputData = window.getInt(31, 6, 2)
VFAT2 = 8 if (inputData < 8 or inputData > 13) else inputData
window.printBox(31, 6, 3, str(VFAT2), "Input", "left")

# Test if VFAT2 is running
if ((glib.getVFAT2(8, "ctrl0") & 0x1) != 0x1):
    # Error
    window.printLine(8, "VFAT2 not running!", "Error", "center")

else:

    # Limits select
    window.printBox(0, 8, 27, "Scan latency from [0-255]:", "Default", "left")
    inputData = window.getInt(27, 8, 3)
    minimumValue = 0 if (inputData < 0 or inputData > 255)  else inputData
    window.printBox(27, 8, 3, str(minimumValue), "Input", "left")

    window.printBox(32, 8, 4, "to", "Default", "left")
    inputData = window.getInt(35, 8, 3)
    maximumValue = 255 if (inputData < 0 or inputData > 255)  else inputData
    window.printBox(35, 8, 3, str(maximumValue), "Input", "left")

    # Events per threshold
    window.printBox(0, 10, 36, "Number of events per latency [100]:", "Default", "left")
    inputData = window.getInt(36, 10, 5)
    nEvents = 100 if (inputData < 0) else inputData
    window.printBox(36, 10, 5, str(nEvents), "Input", "left")

    # Save results
    window.printBox(0, 12, 4, "Save the results [Y/n]:", "Default", "left")
    inputData = window.getChar(24, 12)
    saveResults = True if (inputData == "y" or inputData == "Y" or inputData == False)  else False
    window.printBox(24, 12, 3, ("Yes" if saveResults else "No"), "Input", "left")

    # Wait before starting
    window.printLine(14, "Press [s] to start the scan.", "Info", "center")
    window.waitForKey("s")

    # Create a plot and its data
    latencies = []
    dataPoints = []

    # Loop over Threshold 1
    for latency in range(minimumValue, maximumValue):

        # Percentage
        percentage = (latency - minimumValue) / (1. * maximumValue - minimumValue) * 100.
        window.printLine(15, "Scanning... (" + str(percentage)[:4] + "%)", "Info", "center")

        # Set Threshold 1
        glib.setVFAT2(VFAT2, "latency", latency)

        # Send Resync signal
        glib.set("oh_resync", 0x1)

        # Empty tracking fifo
        glib.set("glib_empty_tracking_data", 0)

        # Efficiency variable
        hitCount = 0.

        # Read tracking packets
        for i in range(0, nEvents):

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

        hitCount /= (nEvents * 1.)

        # Add data
        latencies.append(latency)
        dataPoints.append(hitCount)

        # Update plot
        #graph(latencies, dataPoints, 0, 255, 0, 1, "Latency", "Percentage of hits")

        # Wait a bit
        time.sleep(0.1)

    # Restore old parameters
    glib.setVFAT2(VFAT2, "latency", 0)

    # Write to file
    if (saveResults):
        fileName = "../../test-beam-data/latency/" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
        f = open(fileName,"w")
        f.write("Latency Scan\n")
        f.write("Time: " + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n")
        f.write("VFAT2: " + str(VFAT2) + "\n")
        f.write("Number of events: " + str(nEvents) + "\n")
        f.write("_".join(map(str, latencies)) + "\n")
        f.write("_".join(map(str, dataPoints)) + "\n")
        f.close()

    # Success
    window.printLine(15, "Scan finished!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
