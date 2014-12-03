# System imports
import time
from kernel import *

# Create window
window = Window("Scan a VFAT2's latency")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

#########################################
#   Introduction Window                 #
#########################################

window.clear(1)
window.printLine(1, "Instructions", "Subtitle")
window.printLine(3, "This program allows you to perform a latency scan for one VFAT2.")
window.printLine(4, "For this scan to work, the VFAT2 has to be running and be biased.")
window.printLine(6, "The program will ask you what VFAT2 you want to scan, what the range")
window.printLine(6, "of the scan has to be, and what the number of events per value has to be.")
window.printLine(7, "You can stop the scan at any moment by pressing [Ctrl+C].")
window.printLine(-2, "Hint: here is what to do next (possible actions are always shown here)")
window.printLine(-1, "Press [c] to continue.", "Options")
window.waitForKey("c")

#########################################
#   Parameters                          #
#########################################

window.clear(1)
window.printLine(1, "Parametrization of the scan", "Subtitle")

while (True):
    # Clear line
    window.clear(2, 1)
    # Get a VFAT2 number
    window.printLine(-1, "You have to specify which VFAT2 you want to scan.", "Options")
    vfat2ID = window.inputInt(3, "Select a VFAT2 to scan [8-13]:", 2, 8, 13, 8)
    # Test if VFAT2 is running
    if (glib.isVFAT2Running(vfat2ID) == False):
        # Error
        window.printLine(3, "The selected VFAT2 is not running!", "Error")
        # Timeout
        time.sleep(3)
    else: break

# Limits select
window.printLine(-1, "You have to specify the limits of the scan.", "Options")
minimumValue = window.inputInt(5, "Scan latency from [0-255]:", 3, 0, 255, 0)
maximumValue = window.inputIntShifted(32, 5, "to ["+str(minimumValue)+"-255]:", 3, minimumValue, 255, 255)

# Events per threshold
window.printLine(-1, "You have to specify the number of events to take per value.", "Options")
nEvents = window.inputInt(7, "Number of events per value [1-99999] (100):", 5, 1, 99999, 100)

#########################################
#   Scan                                #
#########################################

window.printLine(1, "Scan control", "Subtitle")

# Wait before starting
window.printLine(-1, "The scan is ready to be started. Press [s] to start.", "Options")
window.printLine(9, "Press [s] to start the scan.", "Info", "center")
window.waitForKey("s")
window.printLine(-1, "Scan in progress...", "Options")
window.printLine(9, "Preparing the scan...", "Info", "center")

# Save VFAT2's parameters
vfat2Parameters = glib.saveVFAT2(vfat2ID)

# Open the save file
save = Save("latency")
save.writePair("VFAT2", vfat2ID)
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
    event = 0

    # Read tracking packets
    while (event < nEvents):

        # Percentage
        percentage = ((latency - minimumValue) * nEvents + event) / ((maximumValue - minimumValue) * nEvents * 1.) * 100.
        window.printLine(9, "Scanning... (" + str(percentage)[:5] + "%)", "Info", "center")

        # Get a tracking packet (with a limit)
        while (True):
            if (glib.get("glib_request_tracking_data") == 0x1): break
            # else: glib.set("oh_lv1a", 1)

        packet1 = glib.get("glib_tracking_data_1")
        packet2 = glib.get("glib_tracking_data_2")
        packet3 = glib.get("glib_tracking_data_3")
        packet4 = glib.get("glib_tracking_data_4")
        packet5 = glib.get("glib_tracking_data_5")

        chipid = (0x00ff0000 & packet5) >> 16
        # if (chipid == vfat2Parameters["chipid0"]): event += 1

        data1 = ((0x0000ffff & packet5) << 16) | ((0xffff0000 & packet4) >> 16)
        data2 = ((0x0000ffff & packet4) << 16) | ((0xffff0000 & packet3) >> 16)
        data3 = ((0x0000ffff & packet3) << 16) | ((0xffff0000 & packet2) >> 16)
        data4 = ((0x0000ffff & packet2) << 16) | ((0xffff0000 & packet1) >> 16)

        if (data1 + data2 + data3 + data4 != 0): hitCount += 1.

        event += 1

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
window.printLine(9, "Scan finished!", "Success", "center")
window.printLine(-1, "Scan in finished. Press [q] to quit.", "Options")
window.printLine(10, "Scan in finished. Press [q] to quit.", "Info", "center")
window.waitForKey("q")

# Close window
window.close()
