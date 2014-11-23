# System imports
from system import *

# Create window
window = Window("Read a GLIB or OptoHybrid register")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Get a register address
window.printBox(0, 4, 26, "Register address [0-28]:", "Default", "left")
window.printBox(0, 5, 26, "0: GLIB error cnt")
window.printBox(26, 5, 26, "1: GLIB VFAT2 RX cnt")
window.printBox(52, 5, 26, "2: GLIB VFAT2 TX cnt")
window.printBox(0, 6, 26, "3: GLIB regs RX cnt")
window.printBox(26, 6, 26, "4: GLIB regs TX cnt")
window.printBox(52, 6, 26, "5: Tracking data size")
window.printBox(0, 7, 26, "6: GLIB firmware version")
window.printBox(26, 7, 26, "7: GLIB SBit select")
window.printBox(52, 7, 26, "8: OH error cnt")
window.printBox(0, 8, 26, "9: OH VFAT2 RX cnt")
window.printBox(26, 8, 26, "10: OH VFAT2 TX cnt")
window.printBox(52, 8, 26, "11: OH regs RX cnt")
window.printBox(0, 9, 26, "12: OH regs TX cnt")
window.printBox(26, 9, 26, "13: OH firmware version")
window.printBox(52, 9, 26, "14: OH trigger source")
window.printBox(0, 10, 26, "15: OH SBit select")
window.printBox(26, 10, 26, "16: OH VFAT2 clk source")
window.printBox(52, 10, 26, "17: OH VFAT2 clk fallback")
window.printBox(0, 11, 26, "18: OH CDCE clk source")
window.printBox(26, 11, 26, "19: OH CDCE clk fallback")
window.printBox(52, 11, 26, "20: OH ext LV1A cnt")
window.printBox(0, 12, 26, "21: OH int LV1A cnt")
window.printBox(26, 12, 26, "22: OH del LV1A cnt")
window.printBox(52, 12, 26, "23: OH LV1A cnt")
window.printBox(0, 13, 26, "24: OH int Cal cnt")
window.printBox(26, 13, 26, "25: OH del Cal cnt")
window.printBox(52, 13, 26, "36: OH Cal cnt")
window.printBox(0, 14, 26, "27: OH Resync cnt")
window.printBox(26, 14, 26, "28: OH BC0 cnt")

inputData = window.getInt(26, 4, 2)
regId = 0 if (inputData < 0 or inputData > 28) else inputData
window.printBox(26, 4, 2, str(regId), "Input", "left")

# Change the register
if (regId == 0):
    regValue = glib.get("glib_error_counter")
elif (regId == 1):
    regValue = glib.get("glib_vfat2_rx_counter")
elif (regId == 2):
    regValue = glib.get("glib_vfat2_tx_counter")
elif (regId == 3):
    regValue = glib.get("glib_reg_rx_counter")
elif (regId == 4):
    regValue = glib.get("glib_reg_tx_counter")
elif (regId == 5):
    regValue = glib.get("glib_tracking_data_occupancy")
elif (regId == 6):
    regValue = glib.get("glib_firmware_version")
elif (regId == 7):
    regValue = glib.get("glib_sbit_select")
elif (regId == 8):
    regValue = glib.get("oh_error_counter")
elif (regId == 9):
    regValue = glib.get("oh_vfat2_rx_counter")
elif (regId == 10):
    regValue = glib.get("oh_vfat2_tx_counter")
elif (regId == 11):
    regValue = glib.get("oh_reg_rx_counter")
elif (regId == 12):
    regValue = glib.get("oh_reg_tx_counter")
elif (regId == 13):
    regValue = glib.get("oh_firmware_version")
elif (regId == 14):
    regValue = glib.get("oh_trigger_source")
elif (regId == 15):
    regValue = glib.get("oh_sbit_select")
elif (regId == 16):
    regValue = glib.get("oh_vfat2_src_select")
elif (regId == 17):
    regValue = glib.get("oh_vfat2_fallback")
elif (regId == 18):
    regValue = glib.get("oh_cdce_src_select")
elif (regId == 19):
    regValue = glib.get("oh_cdce_fallback")
elif (regId == 20):
    regValue = glib.get("oh_ext_lv1a_counter")
elif (regId == 21):
    regValue = glib.get("oh_int_lv1a_counter")
elif (regId == 22):
    regValue = glib.get("oh_del_lv1a_counter")
elif (regId == 23):
    regValue = glib.get("oh_lv1a_counter")
elif (regId == 24):
    regValue = glib.get("oh_int_calpulse_counter")
elif (regId == 25):
    regValue = glib.get("oh_del_calpulse_counter")
elif (regId == 26):
    regValue = glib.get("oh_calpulse_counter")
elif (regId == 27):
    regValue = glib.get("oh_resync_counter")
elif (regId == 28):
    regValue = glib.get("oh_bc0_counter")

# Success
window.printLine(16, "Read value: " + hex(regValue), "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
