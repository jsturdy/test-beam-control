# System imports
import sys, os
from system import *

# Create window
window = Window("Reset counters")

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
window.printLine(7, "Press [s] to reset the counters or [ctrl+c] to quit", "Info", "center")

# Wait for Start signal
while(True):
    c = window.getChar()
    if (c == ord('s')):
        break

# Bias front-end
glib.set('glib_reset_error_counter', 0)
glib.set('glib_reset_vfat2_rx_counter', 0)
glib.set('glib_reset_vfat2_tx_counter', 0)
glib.set('glib_reset_reg_rx_counter', 0)
glib.set('glib_reset_reg_tx_counter', 0)

glib.set('oh_reset_error_counter', 0)
glib.set('oh_reset_vfat2_rx_counter', 0)
glib.set('oh_reset_vfat2_tx_counter', 0)
glib.set('oh_reset_reg_rx_counter', 0)
glib.set('oh_reset_reg_tx_counter', 0)

glib.set('oh_reset_ext_lv1a_counter', 0)
glib.set('oh_reset_int_lv1a_counter', 0)
glib.set('oh_reset_del_lv1a_counter', 0)
glib.set('oh_reset_lv1a_counter', 0)
glib.set('oh_reset_int_calpulse_counter', 0)
glib.set('oh_reset_del_calpulse_counter', 0)
glib.set('oh_reset_calpulse_counter', 0)
glib.set('oh_reset_resync_counter', 0)
glib.set('oh_reset_bc0_counter', 0)

# Design
window.printLine(8, "Counters reseted", "Success", "center")
window.printLine(9, "Press [q] to quit the program", "Warning", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
