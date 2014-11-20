# System imports
import sys, signal, time
from IPBusFunctions import *
from window import *
import matplotlib.pyplot as plt

####################### PARAMETERS #######################

IPreampIn = 0xA8
IPreampFeed = 0x50
IPreampOut = 0x96
IShaper = 0x96
IShaperFeed = 0x64
IComp = 0x78
VThreshold2 = 0x0

numberOfEvents = 50


# Create window
window = Window("S-Curves")

# Get GLIB access
glib = GLIB('192.168.0.115', 'glibAddrTable.dat')

# Print GLIB firmware version
glib_firmware_version = glib.get('info_1_10')
window.printBox(0, 4, 40, "GLIB firmware version: ", "Default", "right")
window.printBox(40, 4, 40, hex(glib_firmware_version), "Default", "left")

# Print OptoHybrid firmware version
oh_firmware_version = glib.get('opto_1_87')
window.printBox(0, 5, 40, "OptoHybrid firmware version: ", "Default", "right")
window.printBox(40, 5, 40, hex(oh_firmware_version), "Default", "left")

# Design
window.printLine(7, "Front-end biasing", "Info", "center")

# Front-end bias
glib.set('vfat2_8_ipreampin', IPreampIn)
window.printBox(0, 9, 40, "IPreampIn: ", "Default", "right")
window.printBox(40, 9, 40, hex(IPreampIn), "Default", "left")

glib.set('vfat2_8_ipreampfeed', IPreampFeed)
window.printBox(0, 10, 40, "IPreampFeed: ", "Default", "right")
window.printBox(40, 10, 40, hex(IPreampFeed), "Default", "left")

glib.set('vfat2_8_ipreampout', IPreampOut)
window.printBox(0, 11, 40, "IPreampOut: ", "Default", "right")
window.printBox(40, 11, 40, hex(IPreampOut), "Default", "left")

glib.set('vfat2_8_ishaper', IShaper)
window.printBox(0, 12, 40, "IShaper: ", "Default", "right")
window.printBox(40, 12, 40, hex(IShaper), "Default", "left")

glib.set('vfat2_8_ishaperfeed', IShaperFeed)
window.printBox(0, 13, 40, "IShaperFeed: ", "Default", "right")
window.printBox(40, 13, 40, hex(IShaperFeed), "Default", "left")

glib.set('vfat2_8_icomp', IComp)
window.printBox(0, 14, 40, "IComp: ", "Default", "right")
window.printBox(40, 14, 40, hex(IComp), "Default", "left")

glib.set('vfat2_8_vthresdhol2', VThreshold2)
window.printBox(0, 15, 40, "VThreshold2: ", "Default", "right")
window.printBox(40, 15, 40, hex(VThreshold2), "Default", "left")

# Design
window.printLine(17, "Press [s] to start scanning VThreshold1", "Success", "center")

# Wait for Start signal
while(True):
    c = window.getChar()
    if (c == ord('s')):
        break

# Start VFAT2
glib.set('vfat2_8_ctrl0', 0x37)

# Send Resync signal
glib.set('opto_1_66', 0x1)

# Design
window.printBox(0, 19, 40, "VThreshold1: ", "Default", "right")
window.printBox(0, 20, 40, "Percentage: ", "Default", "right")

# Create a plot and its data
plt.ion()
dataPoints = []

# Loop over Threshold 1
for VThreshold1 in range(0, 255):

    # Design
    window.printBox(40, 19, 40, hex(VThreshold1), "Default", "left")

    # Set Threshold 1
    glib.set('vfat2_8_vthresdhol1', VThreshold1)

    # Send Resync signal
    glib.set('opto_1_66', 0x1)

    # Empty tracking fifo
    glib.set('info_1_12', 0x0)

    # Efficiency variable
    hitCount = 0.

    # Read tracking packets
    for i in range(0, numberOfEvents):

        # Design
        percentage = (VThreshold1 * numberOfEvents + i) / (numberOfEvents * 255.) * 100.
        window.printBox(40, 20, 40, str(percentage)[:5] + "%", "Default", "left")

        # Send 5 LV1A signal (to be sure...)
        glib.set('opto_1_64', 0x1)
        glib.set('opto_1_64', 0x1)
        glib.set('opto_1_64', 0x1)
        glib.set('opto_1_64', 0x1)
        glib.set('opto_1_64', 0x1)
        glib.set('opto_1_64', 0x1)

        # Get a tracking packet (with a limit)
        while (True):

            # Request new data
            isNewData = glib.get("tracking_1_0")

            if (isNewData == 0x1):
                break

        # packet1 = glib.get("tracking_1_1") >> 16
        # packet2 = glib.get("tracking_1_2")
        packet3 = glib.get("tracking_1_3")
        # packet4 = glib.get("tracking_1_4")
        # packet5 = 0x0000ffff & glib.get("tracking_1_5")

        # if (packet1 + packet2 + packet3 + packet4 + packet5 != 0):
        if ((packet3 & 0x1) != 0):
            hitCount += 1.

    # Add data
    dataPoints.append(hitCount / numberOfEvents)

    # Update plot
    plt.plot(dataPoints)
    plt.axis([0, 255, 0, 1])
    plt.draw()
    plt.clf()

    # Wait a bit
    time.sleep(0.1)

# Stop VFAT2
glib.set('vfat2_8_ctrl0', 0x0)

# Design
window.printLine(22, "Press [q] to quit the program", "Warning", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()

# while (True):

#     # Loop until we get data

#     while (True):

#         # Request new data
#         isNewData = get(glib, "tracking_1_0")

#         if (isNewData == 0x1):
#             break

#     packet1 = get(glib, "tracking_1_1")
#     packet2 = get(glib, "tracking_1_2")
#     packet3 = get(glib, "tracking_1_3")
#     packet4 = get(glib, "tracking_1_4")
#     packet5 = get(glib, "tracking_1_5")
#     packet6 = get(glib, "tracking_1_6")


#     bc = (0x0fff0000 & packet6) >> 16
#     ec = (0x00000ff0 & packet6) >> 4
#     flags = 0x0000000f & packet6
#     chipid = (0x0fff0000 & packet5) >> 16

#     print hex(bc), hex(ec), hex(flags), hex(chipid)


#     raw_input("Press [Enter] to readout data...")


