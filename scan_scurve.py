#!/bin/env python

# System imports
import time
from kernel import *


import uhal

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s", "--slot", type="int", dest="slot",
		  help="slot in uTCA crate", metavar="slot", default=4)

parser.add_option("-o", "--links", type="string", dest="activeLinks", action='append',
		  help="pair of connected optical links (GLIB,OH)", metavar="activeLinks", default=[])
(options, args) = parser.parse_args()

links = {}
for link in options.activeLinks:
	pair = map(int, link.split(","))
	links[pair[0]] = pair[1]
print "links", links

uhal.setLogLevelTo( uhal.LogLevel.FATAL )

if not links.keys():
    print "No optical links specified, exiting"
    exit(1)

# Create window
window = Window("S-Curve")

# Get GLIB access
glib = GLIB(options.slog,links)
glib.setWindow(window)

# Warning
window.printLine(1, "For this scan to work, the VFAT2 has to be biased and running!", "Warning", "center")

# Get a VFAT2 number
vfat2ID = window.inputInt(2, "Select a VFAT2 to scan [8-13]:", 2, 8, 13, 8)

# Test if VFAT2 is running
if (glib.isVFAT2Present(vfat2ID) == False):
    # Error
    window.printLine(2, "The selected VFAT2 is not present!", "Error", "center")

else:
    # Events per threshold
    threshold = window.inputInt(3, "Threshold value [0-255] (30):", 3, 0, 255, 30)

    # Limits select
    minimumValue = window.inputInt(4, "Scan calibration from [0-255]:", 3, 0, 255, 0)
    maximumValue = window.inputIntShifted(36, 4, "to ["+str(minimumValue)+"-255]:", 3, minimumValue, 255, 255)

    # Events per threshold
    nEvents = window.inputInt(5, "Number of events per value [1-99999] (100):", 5, 1, 99999, 100)

    # Wait before starting
    window.printLine(7, "Press [s] to start the scan.", "Info", "center")
    window.waitForKey("s")
    window.printLine(8, "Preparing the scan...", "Info", "center")

    # Save VFAT2's parameters
    vfat2Parameters = glib.saveVFAT2(vfat2ID)

    # Open the save file
    save = Save("scurve")
    save.writeLine("Started a SCurve of VFAT2 #"+str(vfat2ID)+" from "+str(minimumValue)+ " to "+str(maximumValue)+ " with "+str(nEvents)+" events and threshold "+str(threshold))
    save.writeLine("--- VFAT2 #"+str(vfat2ID)+" configuration ---")
    save.writeDict(vfat2Parameters)
    save.writeLine("--- Data points ---")

    # Common parameters
    glib.setVFAT2(vfat2ID, "ContReg0", 119)
    glib.setVFAT2(vfat2ID, "ContReg2", 112)
    glib.setVFAT2(vfat2ID, "Latency", 10)
    glib.setVFAT2Channel(vfat2ID, 8, 64)
    # glib.setVFAT2Channel(vfat2ID, 9, 64)
    # glib.setVFAT2Channel(vfat2ID, 10, 64)
    glib.setVFAT2(vfat2ID, "VThreshold1", threshold)
    glib.setVFAT2(vfat2ID, "VCal", 255)

    # Create a plot and its data
    vcalValues = []
    hitValues = []

    # Loop over Threshold 1
    for vcal in range(minimumValue, maximumValue):

        # Set threshold
        glib.setVFAT2(vfat2ID, "Latency", vcal)
        glib.disableVFAT2(vfat2ID)

        # Send Resync signal
        glib.sendResync()

        # Empty tracking fifo
        glib.flushFIFO()

        # Efficiency variable
        hitCount = 0.
        event = 0

        glib.enableVFAT2(vfat2ID)
        # Read tracking packets
        while (event < nEvents):

            # Percentage
            percentage = ((vcal - minimumValue) * nEvents + event) / ((maximumValue - minimumValue) * nEvents * 1.) * 100.
            window.printLine(8, "Scanning... (" + str(percentage)[:5] + "%)", "Info", "center")

            # Get a tracking packet (with a limit)
            while (True):
                if (glib.get("glib_request_tracking_data") == 0x1): break
                else: glib.set("oh_lv1a_and_calpulse", 40)

            packet1 = glib.get("glib_tracking_data_1")
            packet2 = glib.get("glib_tracking_data_2")
            packet3 = glib.get("glib_tracking_data_3")
            packet4 = glib.get("glib_tracking_data_4")
            packet5 = glib.get("glib_tracking_data_5")

            # Check Chipid
            chipid = (0x00ff0000 & packet5) >> 16
            #if (chipid != vfat2Parameters["chipid0"]): continue
            #else: event += 1
            event += 1


            data1 = ((0x00007fff & packet5) << 16) | ((0xffff0000 & packet4) >> 16)
            data2 = ((0x0000ffff & packet4) << 16) | ((0xffff0000 & packet3) >> 16)
            data3 = ((0x0000ffff & packet3) << 16) | ((0xffff0000 & packet2) >> 16)
            data4 = ((0x0000ffff & packet2) << 16) | ((0xffff0000 & packet1) >> 16)

            if (data1 + data2 + data3 + data4 != 0): hitCount += 1.

            event += 1

        hitCount /= (nEvents * 1.)

        # Save the points
        save.writePair(vcal, hitCount)

        # Add data
        vcalValues.append(vcal)
        hitValues.append(hitCount)

        # Update plot
        graph(vcalValues, hitValues, minimumValue, maximumValue, 0, 1, "Threshold", "Percentage of hits")

    # Reset the VFAT2 parameters
    glib.restoreVFAT2(vfat2ID, vfat2Parameters)
    glib.setVFAT2Channel(vfat2ID, 8,  0)
    glib.setVFAT2Channel(vfat2ID, 9,  0)
    glib.setVFAT2Channel(vfat2ID, 10, 0)

    # Close the save file
    save.close()

    # Success
    window.printLine(9, "Scan finished!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
