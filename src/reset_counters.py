# System imports
from system import *

# Create window
window = Window("Reset the counters on the GLIB and the OptoHybrid")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Design
window.printLine(4, "Press [s] to reset the counters.", "Info", "center")
window.waitForKey("s")

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

# Log the changes
save = Save("log")
save.writeLine("Counters reseted")
save.close()

# Design
window.printLine(5, "Counters reseted!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
