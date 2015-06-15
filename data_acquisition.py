# System imports
import time
from kernel import *

# Create window
window = Window("Manage data acquisition")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

#
save = False
nEvents = 0

#########################################
#   Introduction Window                 #
#########################################

def introWindow():
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Instructions", "Subtitle")
    window.printLine(3, "This program allows you manage the acquisition of data.")
    window.printLine(5, "You will be asked to enter a run number for the acquisition of data.")
    window.printLine(6, "Once this is done, you will be able to:")
    window.printLine(7, "Start/restart the data tacking by pressing [s].")
    window.printLine(8, "Start a new run by pressing [n].")
    window.printLine(9, "Empty the buffers by pressing [e].")
    window.printLine(10, "Quit the program by pressing [q].")
    window.printLine(11, "As you can see, when a key performs an action, it is placed between brackets.")
    window.printLine(13, "The plot that appears when tacking data is the beam profile.")
    window.printLine(15, "You can always exit the program by pressing [Ctrl+C].")
    window.printLine(-2, "Hint: here is what to do next (possible actions are always shown here)")
    window.printLine(-1, "Press [c] to continue.", "Options")
    # Go to non-blocking mode
    window.disableBlocking()
    #
    while (True):
        if (window.getChr() == ord('c')): return

#########################################
#   Main window: choose what to do      #
#########################################

def mainWindow(runNumber):
    global glib, window, nEvents
    # Design
    window.clear(1)
    window.printLine(1, "Run management", "Subtitle")
    window.printLine(3, "Run #"+str(runNumber)+" is currently paused, what do you want to do?", "Highlight")
    window.printLabel(0, 5, 35, "Number of events in the run:", nEvents)
    window.printLine(-1, "Actions: [q]uit, [s]tart the run, [n]ew run, [e]mpty buffers", "Options")
    # Go to non-blocking mode
    window.disableBlocking()
    # Stay in this window until command select
    while (True):
        select = window.getChr()
        if (select == ord('q')): return -1
        elif (select == ord('s')): return 1
        elif (select == ord('n')): return 2
        elif (select == ord('e')): return 3

#########################################
#   Empty the buffers                   #
#########################################

def emptyBuffersWindow():
    global glib, window
    # Design
    window.clear(1)
    window.printLine(1, "Emptying the buffers", "Subtitle")
    window.printLine(3, "Waiting for confirmation before emptying the buffers.", "Highlight")
    window.printLine(-1, "Empty the buffers? [y]es, [n]o", "Options")
    # Go to non-blocking mode
    window.disableBlocking()
    #
    while (True):
        pressedKey = window.getChr()
        if (pressedKey == ord('n')): return
        elif (pressedKey == ord('y')): break
    #
    glib.set("glib_empty_tracking_data_0", 1)
    glib.set("glib_empty_tracking_data_1", 1)
    glib.set("glib_empty_tracking_data_2", 1)
    #
    window.printLine(-1, "Buffers emptied!", "Success")
    #
    time.sleep(2)

#########################################
#   Get data                            #
#########################################

def getDataWindow():
    global glib, window, save, nEvents
    # Design
    window.clear(1)
    window.printLine(1, "Acquiring data", "Subtitle")
    window.printLine(-1, "Actions: s[t]op the acquisition", "Options")
    # Go to non-blocking mode
    window.disableBlocking()
    #
    strips = [0] * 128
    #
    while (True):
        window.printLine(3, str(nEvents) + " events saved during this acquisition!", "Info")

        packet1 = packet2 = packet3 = packet4 = packet5 = packet6 = packet7 = 0

        # Get a tracking packet (with a limit)
        while (True):
            if (glib.get("glib_track_0_req") == 0x1): 
                packet1 = glib.get("glib_track_0_d1")
                packet2 = glib.get("glib_track_0_d2")
                packet3 = glib.get("glib_track_0_d3")
                packet4 = glib.get("glib_track_0_d4")
                packet5 = glib.get("glib_track_0_d5")
                packet6 = glib.get("glib_track_0_d6")
                packet7 = glib.get("glib_track_0_d7")
                break
            # if (glib.get("glib_track_1_req") == 0x1): 
            #     packet1 = glib.get("glib_track_1_d1")
            #     packet2 = glib.get("glib_track_1_d2")
            #     packet3 = glib.get("glib_track_1_d3")
            #     packet4 = glib.get("glib_track_1_d4")
            #     packet5 = glib.get("glib_track_1_d5")
            #     packet6 = glib.get("glib_track_1_d6")
            #     packet7 = glib.get("glib_track_1_d7")
            #     break
            if (glib.get("glib_track_2_req") == 0x1): 
                packet1 = glib.get("glib_track_2_d1")
                packet2 = glib.get("glib_track_2_d2")
                packet3 = glib.get("glib_track_2_d3")
                packet4 = glib.get("glib_track_2_d4")
                packet5 = glib.get("glib_track_2_d5")
                packet6 = glib.get("glib_track_2_d6")
                packet7 = glib.get("glib_track_2_d7")
                break
            for i in range(0, 100):
               if (window.getChr() == ord('t')): return
        #

        # Format data
        bc = str((0x0fff0000 & packet6) >> 16)
        ec = str((0x00000ff0 & packet6) >> 4)
        chipid = str((0x0fff0000 & packet5) >> 16)
        data1 = bin(((0x0000ffff & packet5) << 16) | ((0xffff0000 & packet4) >> 16))[2:].zfill(32)
        data2 = bin(((0x0000ffff & packet4) << 16) | ((0xffff0000 & packet3) >> 16))[2:].zfill(32)
        data3 = bin(((0x0000ffff & packet3) << 16) | ((0xffff0000 & packet2) >> 16))[2:].zfill(32)
        data4 = bin(((0x0000ffff & packet2) << 16) | ((0xffff0000 & packet1) >> 16))[2:].zfill(32)
        crc = str(0x0000ffff & packet1)
        bx = str(packet7)
        # Save data
        save.writeInt(packet6)
        save.writeInt(packet5)
        save.writeInt(packet4)
        save.writeInt(packet3)
        save.writeInt(packet2)
        save.writeInt(packet1)
        save.writeInt(packet7)
        save.write('\n')
        # Show histogram
        for i in range(0, 31):
            strips[i] += (1 if (data1[i] == '1') else 0)
            strips[i + 32] += (1 if (data2[i] == '1') else 0)
            strips[i + 64] += (1 if (data3[i] == '1') else 0)
            strips[i + 96] += (1 if (data4[i] == '1') else 0)
        #
        graph1D(strips, 0, 127)
        # Data
        window.printLine(5, "Information about the last event:")
        window.printLabel(0, 6, 40, "BC:", bc)
        window.printLabel(0, 7, 40, "EC:", ec)
        window.printLabel(0, 8, 40, "ChipID:", chipid)
        window.printLabel(0, 9, 40, "Data 1:", data1)
        window.printLabel(0, 10, 40, "Data 2:", data2)
        window.printLabel(0, 11, 40, "Data 3:", data3)
        window.printLabel(0, 12, 40, "Data 4:", data4)
        window.printLabel(0, 13, 40, "CRC:", crc)
        window.printLabel(0, 14, 40, "BX:", bx)
        #
        nEvents += 1

#########################################
#   Main program                        #
#########################################

isConnected = False
# Show the intro
introWindow()
# Program loop
while (True):
    if (isConnected == False):
        # Clear the screen
        window.clear()
        # Go to blocking mode
        window.enableBlocking()
        # Enter a run number
        window.printLine(1, "Run selection", "Subtitle")
        window.printLine(-1, "You have to specify a run number.", "Options")
        runNumber = window.inputInt(3, "Run number [0-99999]:", 5, 0, 99999, 0)
        # Save VFAT2's parameters
        systemRegisters = glib.saveSystem()
        vfat2Parameters = [None] * 6
        vfat2Parameters[0] = glib.saveVFAT2(8)
        vfat2Parameters[1] = glib.saveVFAT2(9)
        vfat2Parameters[2] = glib.saveVFAT2(10)
        vfat2Parameters[3] = glib.saveVFAT2(11)
        vfat2Parameters[4] = glib.saveVFAT2(12)
        vfat2Parameters[5] = glib.saveVFAT2(13)
        # Open the save file
        save = Save("tracking")
        save.writeLine("Started run #"+str(runNumber))
        save.writeLine("--- System configuration ---")
        save.writeDict(systemRegisters)
        save.writeLine("--- VFAT2 #8 configuration ---")
        save.writeDict(vfat2Parameters[0])
        save.writeLine("--- VFAT2 #9 configuration ---")
        save.writeDict(vfat2Parameters[1])
        save.writeLine("--- VFAT2 #10 configuration ---")
        save.writeDict(vfat2Parameters[2])
        save.writeLine("--- VFAT2 #11 configuration ---")
        save.writeDict(vfat2Parameters[3])
        save.writeLine("--- VFAT2 #12 configuration ---")
        save.writeDict(vfat2Parameters[4])
        save.writeLine("--- VFAT2 #13 configuration ---")
        save.writeDict(vfat2Parameters[5])
        save.writeLine("--- Events ---")
        save.switchToBinary()
        #
        isConnected = True
    else:
        nextState = mainWindow(runNumber)

        if (nextState == -1): break
        elif (nextState == 1): getDataWindow()
        elif (nextState == 2): isConnected = False
        elif (nextState == 3): emptyBuffersWindow()

# Close window
window.close()
