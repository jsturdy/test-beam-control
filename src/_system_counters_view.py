# System imports
from kernel import *

# Create window
window = Window("View the counters of the GLIB and the OptoHybrid")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

while (True):

    # Get values
    value = glib.get("glib_error_counter")
    window.printBox(0, 4, 30, "GLIB errors:", "Default", "left")
    window.printBox(30, 4, 25, str(value), "Default", "left")

    value = glib.get("glib_vfat2_rx_counter")
    window.printBox(0, 5, 30, "GLIB VFAT2 RX:", "Default", "left")
    window.printBox(30, 5, 25, str(value), "Default", "left")

    value = glib.get("glib_vfat2_tx_counter")
    window.printBox(0, 6, 30, "GLIB VFAT2 TX:", "Default", "left")
    window.printBox(30, 6, 25, str(value), "Default", "left")

    value = glib.get("glib_reg_rx_counter")
    window.printBox(0, 7, 30, "GLIB registers RX:", "Default", "left")
    window.printBox(30, 7, 25, str(value), "Default", "left")

    value = glib.get("glib_reg_tx_counter")
    window.printBox(0, 8, 30, "GLIB registers TX:", "Default", "left")
    window.printBox(30, 8, 25, str(value), "Default", "left")

    value = glib.get("oh_error_counter")
    window.printBox(0, 9, 30, "OptoHybrid errors:", "Default", "left")
    window.printBox(30, 9, 25, str(value), "Default", "left")

    value = glib.get("oh_vfat2_rx_counter")
    window.printBox(0, 10, 30, "OptoHybrid VFAT2 RX:", "Default", "left")
    window.printBox(30, 10, 25, str(value), "Default", "left")

    value = glib.get("oh_vfat2_tx_counter")
    window.printBox(0, 11, 30, "OptoHybrid VFAT2 TX:", "Default", "left")
    window.printBox(30, 11, 25, str(value), "Default", "left")

    value = glib.get("oh_reg_rx_counter")
    window.printBox(0, 12, 30, "OptoHybrid registers RX:", "Default", "left")
    window.printBox(30, 12, 25, str(value), "Default", "left")

    value = glib.get("oh_reg_tx_counter")
    window.printBox(0, 13, 30, "OptoHybrid registers TX:", "Default", "left")
    window.printBox(30, 13, 25, str(value), "Default", "left")

    value = glib.get("oh_ext_lv1a_counter")
    window.printBox(0, 14, 30, "External LV1As:", "Default", "left")
    window.printBox(30, 14, 25, str(value), "Default", "left")

    value = glib.get("oh_int_lv1a_counter")
    window.printBox(0, 15, 30, "Internal LV1As:", "Default", "left")
    window.printBox(30, 15, 25, str(value), "Default", "left")

    value = glib.get("oh_del_lv1a_counter")
    window.printBox(0, 16, 30, "Delayed LV1As:", "Default", "left")
    window.printBox(30, 16, 25, str(value), "Default", "left")

    value = glib.get("oh_lv1a_counter")
    window.printBox(0, 17, 30, "Total LV1As:", "Default", "left")
    window.printBox(30, 17, 25, str(value), "Default", "left")

    value = glib.get("oh_int_calpulse_counter")
    window.printBox(0, 18, 30, "Internal LV1As:", "Default", "left")
    window.printBox(30, 18, 25, str(value), "Default", "left")

    value = glib.get("oh_del_calpulse_counter")
    window.printBox(0, 19, 30, "Delayed LV1As:", "Default", "left")
    window.printBox(30, 19, 25, str(value), "Default", "left")

    value = glib.get("oh_calpulse_counter")
    window.printBox(0, 20, 30, "Total LV1As:", "Default", "left")
    window.printBox(30, 20, 25, str(value), "Default", "left")

    value = glib.get("oh_resync_counter")
    window.printBox(0, 21, 30, "Resyncs:", "Default", "left")
    window.printBox(30, 21, 25, str(value), "Default", "left")

    value = glib.get("oh_bc0_counter")
    window.printBox(0, 22, 30, "BC0s:", "Default", "left")
    window.printBox(30, 22, 25, str(value), "Default", "left")

    window.printLine(24, "Press [s] to refresh.", "Info", "center")
    window.waitForKey("s")

# Close window
window.close()
