#!/bin/env python

# System imports
import time
from math import sqrt
from kernel import *

# Create window
window = Window("Scan a VFAT2's DAC")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

#########################################
#   Introduction Window                 #
#########################################

window.clear(1)
window.printLine(1, "Instructions", "Subtitle")
window.printLine(3, "This program allows you to perform a DAC scan for one VFAT2.")
window.printLine(5, "The program will ask you what VFAT2 you want to scan, what DAC you")
window.printLine(6, "want to scan, what the range of the scan has to be, and what the number")
window.printLine(7, "of events per value has to be.")
window.printLine(8, "You can stop the scan at any moment by pressing [Ctrl+C].")
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

# Get the DAC to scan
window.printLine(-1, "You have to specify which DAC you want to scan.", "Options")
window.printBox(0, 6, 20, "1: IPreampIn")
window.printBox(20, 6, 20, "2: IPreampFeed")
window.printBox(40, 6, 20, "3: IPreampOut")
window.printBox(60, 6, 20, "4: IShaper")
window.printBox(0, 7, 20, "5: IShaperFeed")
window.printBox(20, 7, 20, "6: IComp")
window.printBox(40, 7, 20, "7: VThreshold1")
window.printBox(60, 7, 20, "8: VThreshold2")
window.printBox(0, 8, 20, "9: VCal")
DAC = window.inputInt(5, "Select a DAC to scan [1-9]:", 1, 1, 9, 1)

# Limits select
window.printLine(-1, "You have to specify the limits of the scan.", "Options")
minimumValue = window.inputInt(10, "Scan DAC from [0-255]:", 3, 0, 255, 0)
maximumValue = window.inputIntShifted(28, 10, "to ["+str(minimumValue)+"-255]:", 3, minimumValue, 255, 255)

# Events per threshold
window.printLine(-1, "You have to specify the number of measurements to take per value.", "Options")
nEvents = window.inputInt(12, "Number of events per value [0-99999] (100):", 5, 1, 99999, 100)

#########################################
#   Scan                                #
#########################################

window.printLine(1, "Scan control", "Subtitle")

# Wait before starting
window.printLine(-1, "The scan is ready to be started. Press [s] to start.", "Options")
window.printLine(14, "Press [s] to start the scan.", "Info", "center")
window.waitForKey("s")
window.printLine(-1, "Scan in progress...", "Options")
window.printLine(14, "Preparing the scan...", "Info", "center")

# Save VFAT2's parameters
vfat2Parameters = glib.saveVFAT2(vfat2ID)

# Open the save file
save = Save("dac")
save.writeLine("Started a DAC scan on DAC #"+str(DAC)+" of VFAT2 #"+str(vfat2ID)+" from "+str(minimumValue)+ " to "+str(maximumValue)+ " with "+str(nEvents)+" events")
save.writeLine("--- VFAT2 #"+str(vfat2ID)+" configuration ---")
save.writeDict(vfat2Parameters)
save.writeLine("--- Data points ---")
save.writeLine("In\t<x>\tsig(<x>)")

# Change the VFAT2's parameters
glib.setVFAT2(vfat2ID, "ctrl1", DAC)
glib.setVFAT2(vfat2ID, "ctrl0", 0x1)
glib.setVFAT2(vfat2ID, "ipreampin", 0)
glib.setVFAT2(vfat2ID, "ipreampfeed", 0)
glib.setVFAT2(vfat2ID, "ipreampout", 0)
glib.setVFAT2(vfat2ID, "ishaper", 0)
glib.setVFAT2(vfat2ID, "ishaperfeed", 0)
glib.setVFAT2(vfat2ID, "icomp", 0)
glib.setVFAT2(vfat2ID, "vthreshold1", 0)
glib.setVFAT2(vfat2ID, "vthreshold2", 0)
glib.setVFAT2(vfat2ID, "vcal", 0)
glib.set("oh_resync", 1)

# Data values
dacValues = []
adcValues = []

# Loop over DAC
for dacValue in range(minimumValue, maximumValue):

    # Set the DAC
    if (DAC == 1): glib.setVFAT2(vfat2ID, "ipreampin", dacValue)
    elif (DAC == 2): glib.setVFAT2(vfat2ID, "ipreampfeed", dacValue)
    elif (DAC == 3): glib.setVFAT2(vfat2ID, "ipreampout", dacValue)
    elif (DAC == 4): glib.setVFAT2(vfat2ID, "ishaper", dacValue)
    elif (DAC == 5): glib.setVFAT2(vfat2ID, "ishaperfeed", dacValue)
    elif (DAC == 6): glib.setVFAT2(vfat2ID, "icomp", dacValue)
    elif (DAC == 7): glib.setVFAT2(vfat2ID, "vthreshold1", dacValue)
    elif (DAC == 8): glib.setVFAT2(vfat2ID, "vthreshold2", dacValue)
    elif (DAC == 9): glib.setVFAT2(vfat2ID, "vcal", dacValue)

    # Send Resync signal
    glib.set("oh_resync", 0x1)

    # Average ADC value
    sumADC = 0
    sumADC2 = 0
    averageADC = 0
    averageADC2 = 0

    # Get N ADC
    for event in range(0, nEvents):

        # Percentage
        percentage = ((dacValue - minimumValue) * nEvents + event) / ((maximumValue - minimumValue) * nEvents * 1.) * 100.
        window.printLine(14, "Scanning... (" + str(percentage)[:5] + "%)", "Info", "center")

        time.sleep(0.25)

        if (DAC <= 6):
            valueADC = glib.get("oh_adc_i")
            sumADC += valueADC
            sumADC2 += valueADC * valueADC
        else:
            valueADC = glib.get("oh_adc_v")
            sumADC += valueADC
            sumADC2 += valueADC * valueADC

    averageADC = sumADC / (nEvents * 1.)
    averageADC2 = sumADC2 / (nEvents * 1.)

    # Save the points
    #save.writePair(dacValue, averageADC)
    save.writeList([dacValue, averageADC, sqrt(averageADC2 - averageADC * averageADC) / sqrt(nEvents)])

    # Add data
    dacValues.append(dacValue)
    adcValues.append(averageADC)

    # Update plot
    graph(dacValues, adcValues, minimumValue, maximumValue, 0, 1023, "DAC value", "ADC value")

# Reset the VFAT2 parameters
glib.restoreVFAT2(vfat2ID, vfat2Parameters)

# Close the save file
save.close()

# Success
window.printLine(14, "Scan finished!", "Success", "center")
window.printLine(-1, "Scan in finished. Press [q] to quit.", "Options")
window.printLine(15, "Scan in finished. Press [q] to quit.", "Info", "center")
window.waitForKey("q")
# Close window
window.close()
