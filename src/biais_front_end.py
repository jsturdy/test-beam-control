# System imports
import sys, os
from system import *

####################### Default parameters #######################

IPreampIn = 0xA8
IPreampFeed = 0x50
IPreampOut = 0x96
IShaper = 0x96
IShaperFeed = 0x64
IComp = 0x78
VThreshold2 = 0x0

# Create window
window = Window("Front-end bias")

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
window.printLine(7, "Press [Enter] to use the default values", "Info", "center")

# VFAT2 select
window.printBox(0, 9, 40, "VFAT2 to bias: ", "Default", "right")
window.printBox(50, 9, 10, "[8]", "Default", "left")

# Front-end bias
window.printBox(0, 11, 40, "Register  ", "Default", "right")
window.printBox(40, 11, 10, "Value", "Default", "left")
window.printBox(50, 11, 10, "Default", "Default", "left")

window.printBox(0, 12, 40, "IPreampIn: ", "Default", "right")
window.printBox(50, 12, 10, "[" + str(IPreampIn) + "]", "Default", "left")

window.printBox(0, 13, 40, "IPreampFeed: ", "Default", "right")
window.printBox(50, 13, 10, "[" + str(IPreampFeed) + "]", "Default", "left")

window.printBox(0, 14, 40, "IPreampOut: ", "Default", "right")
window.printBox(50, 14, 10, "[" + str(IPreampOut) + "]", "Default", "left")

window.printBox(0, 15, 40, "IShaper: ", "Default", "right")
window.printBox(50, 15, 10, "[" + str(IShaper) + "]", "Default", "left")

window.printBox(0, 16, 40, "IShaperFeed: ", "Default", "right")
window.printBox(50, 16, 10, "[" + str(IShaperFeed) + "]", "Default", "left")

window.printBox(0, 17, 40, "IComp: ", "Default", "right")
window.printBox(50, 17, 10, "[" + str(IComp) + "]", "Default", "left")

window.printBox(0, 18, 40, "VThreshold2: ", "Default", "right")
window.printBox(50, 18, 10, "[" + str(VThreshold2) + "]", "Default", "left")

# Ask values
VFAT2 = window.getInt(40, 9, 10)
IPreampIn_value = window.getInt(40, 12, 10)
IPreampFeed_value = window.getInt(40, 13, 10)
IPreampOut_value = window.getInt(40, 14, 10)
IShaper_value = window.getInt(40, 15, 10)
IShaperFeed_value = window.getInt(40, 16, 10)
IComp_value = window.getInt(40, 17, 10)
VThreshold2_value = window.getInt(40, 18, 10)

if (VFAT2 == -1):
    VFAT2 = 8
if (IPreampIn_value == -1):
    IPreampIn_value = IPreampIn
if (IPreampFeed_value == -1):
    IPreampFeed_value = IPreampFeed
if (IPreampOut_value == -1):
    IPreampOut_value = IPreampOut
if (IShaper_value == -1):
    IShaper_value = IShaper
if (IShaperFeed_value == -1):
    IShaperFeed_value = IShaperFeed
if (IComp_value == -1):
    IComp_value = IComp
if (VThreshold2_value == -1):
    VThreshold2_value = VThreshold2

# Design
window.printLine(20, "Press [s] to bias the front-end or [ctrl+c] to quit", "Info", "center")

# Wait for Start signal
while(True):
    c = window.getChar()
    if (c == ord('s')):
        break

# Test if VFAT2 is present
testVFAT2Present = glib.getVFAT2(VFAT2, 'chipid0')

if (((testVFAT2Present & 0x4000000) >> 26) == 1):
    # Error
    window.printLine(21, "VFAT2 not present!", "Error", "center")

else:
    # Bias front-end
    glib.setVFAT2(VFAT2, 'ipreampin', IPreampIn_value)
    glib.setVFAT2(VFAT2, 'ipreampfeed', IPreampFeed_value)
    glib.setVFAT2(VFAT2, 'ipreampout', IPreampOut_value)
    glib.setVFAT2(VFAT2, 'ishaper', IShaper_value)
    glib.setVFAT2(VFAT2, 'ishaperfeed', IShaperFeed_value)
    glib.setVFAT2(VFAT2, 'icomp', IComp_value)
    glib.setVFAT2(VFAT2, 'vthreshold2', VThreshold2_value)

    glib.set('oh_resync', 0)

    # Success
    window.printLine(21, "Front-end biased", "Success", "center")

# Quit
window.printLine(22, "Press [q] to quit the program", "Warning", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
