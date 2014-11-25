# System imports
import time
from system import *

# Create window
window = Window("Scan a VFAT2's DAC")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Get a VFAT2 number
vfat2ID = window.inputInt(4, "Select a VFAT2 to scan [8-13]:", 2, 8, 13, 8)

# Get the DAC to scan
window.printBox(0, 7, 20, "1: IPreampIn")
window.printBox(20, 7, 20, "2: IPreampFeed")
window.printBox(40, 7, 20, "3: IPreampOut")
window.printBox(60, 7, 20, "4: IShaper")
window.printBox(0, 8, 20, "5: IShaperFeed")
window.printBox(20, 8, 20, "6: IComp")
window.printBox(40, 8, 20, "7: VThreshold1")
window.printBox(60, 8, 20, "8: VThreshold2")
window.printBox(0, 9, 20, "9: VCal")
DAC = window.inputInt(6, "Select a DAC to scan [1-9]:", 1, 1, 9, 1)

# Limits select
minimumValue = window.inputInt(11, "Scan DAC from [0-255]:", 3, 0, 255, 0)
maximumValue = window.inputIntShifted(28, 11, "to ["+str(minimumValue)+"-255]:", 3, minimumValue, 255, 255)

# Events per threshold
nEvents = window.inputInt(13, "Number of events per value (100):", 5, 0, 1000, 100)

# Wait before starting
window.printLine(15, "Press [s] to start the scan.", "Info", "center")
window.waitForKey("s")

# Test if VFAT2 is present
if (glib.isVFAT2(vfat2ID) == False):
    # Error
    window.printLine(16, "The selected VFAT2 is not present!", "Error", "center")
#
else:

    # Save VFAT2's parameters
    vfat2Parameters = glib.saveVFAT2(vfat2ID)

    # Open the save file
    save = Save("dac")
    save.writeDict(vfat2Parameters)
    save.writeLine("-----")

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
        if (DAC == 1):
            glib.setVFAT2(vfat2ID, "ipreampin", dacValue)
        elif (DAC == 2):
            glib.setVFAT2(vfat2ID, "ipreampfeed", dacValue)
        elif (DAC == 3):
            glib.setVFAT2(vfat2ID, "ipreampout", dacValue)
        elif (DAC == 4):
            glib.setVFAT2(vfat2ID, "ishaper", dacValue)
        elif (DAC == 5):
            glib.setVFAT2(vfat2ID, "ishaperfeed", dacValue)
        elif (DAC == 6):
            glib.setVFAT2(vfat2ID, "icomp", dacValue)
        elif (DAC == 7):
            glib.setVFAT2(vfat2ID, "vthreshold1", dacValue)
        elif (DAC == 8):
            glib.setVFAT2(vfat2ID, "vthreshold2", dacValue)
        elif (DAC == 9):
            glib.setVFAT2(vfat2ID, "vcal", dacValue)

        # Send Resync signal
        glib.set("oh_resync", 0x1)

        # Average ADC value
        averageADC = 0

        # Get N ADC
        for event in range(0, nEvents):

            # Percentage
            percentage = ((dacValue - minimumValue) * nEvents + event) / ((maximumValue - minimumValue) * nEvents * 1.) * 100.
            window.printLine(18, "Scanning... (" + str(percentage)[:5] + "%)", "Info", "center")

            time.sleep(0.25)

            if (DAC <= 6):
                averageADC += glib.get("oh_adc_i")
            else:
                averageADC += glib.get("oh_adc_v")

        averageADC /= (nEvents * 1.)

        # Save the points
        save.writePair(dacValue, averageADC)

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
    window.printLine(18, "Scan finished!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
