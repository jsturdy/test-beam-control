# System imports
import time
from kernel import *

# Create window
window = Window("Scan a VFAT2's latency")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Warning
window.printLine(4, "For this scan to work, the VFAT2 has to be biased and running!", "Warning", "center")

# Get a VFAT2 number
vfat2ID = window.inputInt(6, "Select a VFAT2 to scan [8-13]:", 2, 8, 13, 8)

# Test if VFAT2 is running
if ((glib.getVFAT2(8, "ctrl0") & 0x1) != 0x1):
    # Error
    window.printLine(8, "VFAT2 not running!", "Error", "center")

else:

    # Limits select
    minimumValue = window.inputInt(8, "Scan latency from [0-255]:", 3, 0, 255, 0)
    maximumValue = window.inputIntShifted(32, 8, "to ["+str(minimumValue)+"-255]:", 3, minimumValue, 255, 255)

    # Events per threshold
    nEvents = window.inputInt(10, "Number of events per value [0-99999] (100):", 5, 1, 99999, 100)

    # Wait before starting
    window.printLine(12, "Press [s] to start the scan.", "Info", "center")
    window.waitForKey("s")

    # Save VFAT2's parameters
    vfat2Parameters = glib.saveVFAT2(vfat2ID)

    # Open the save file
    save = Save("latency")
    save.writeLine("-----")
    save.writePair("VFAT2 ID", vfat2ID)
    save.writePair("from", minimumValue)
    save.writePair("to", maximumValue)
    save.writePair("events", nEvents)
    save.writeLine("-----")
    save.writeDict(vfat2Parameters)
    save.writeLine("-----")

    # Create a plot and its data
    latencyValues = []
    hitValues = []

    # Loop over latencies
    for latency in range(minimumValue, maximumValue):

        # Set latency
        glib.setVFAT2(vfat2ID, "latency", latency)

        # Send Resync signal
        glib.set("oh_resync", 0x1)

        # Empty tracking fifo
        glib.set("glib_empty_tracking_data", 0)

        # Efficiency variable
        hitCount = 0.

        # Read tracking packets
        for event in range(0, nEvents):

            # Percentage
            percentage = ((latency - minimumValue) * nEvents + event) / ((maximumValue - minimumValue) * nEvents * 1.) * 100.
            window.printLine(13, "Scanning... (" + str(percentage)[:5] + "%)", "Info", "center")

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

        # Save the points
        save.writePair(latency, hitCount)

        # Add data
        latencyValues.append(latency)
        hitValues.append(hitCount)

        # Update plot
        graph(latencyValues, hitValues, minimumValue, maximumValue, 0, 1, "Latency", "Percentage of hits")

    # Reset the VFAT2 parameters
    glib.restoreVFAT2(vfat2ID, vfat2Parameters)

    # Close the save file
    save.close()

    # Success
    window.printLine(13, "Scan finished!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
