# System imports
from kernel import *

# Create window
window = Window("Write a GLIB or OptoHybrid register")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Get a register address
window.printBox(0, 5, 26, "0: GLIB error cnt rst")
window.printBox(26, 5, 26, "1: GLIB VFAT2 RX cnt rst")
window.printBox(52, 5, 26, "2: GLIB VFAT2 TX cnt rst")
window.printBox(0, 6, 26, "3: GLIB regs RX cnt rst")
window.printBox(26, 6, 26, "4: GLIB regs TX cnt rst")
window.printBox(52, 6, 26, "5: GLIB empty tracking")
window.printBox(0, 7, 26, "6: GLIB empty trigger")
window.printBox(26, 7, 26, "7: GLIB SBit select")
window.printBox(52, 7, 26, "8: OH error cnt rst")
window.printBox(0, 8, 26, "9: OH VFAT2 RX cnt rst")
window.printBox(26, 8, 26, "10: OH VFAT2 TX cnt rst")
window.printBox(52, 8, 26, "11: OH regs RX cnt rst")
window.printBox(0, 9, 26, "12: OH regs TX cnt rst")
window.printBox(26, 9, 26, "13: OH LV1A")
window.printBox(52, 9, 26, "14: OH Calpulse")
window.printBox(0, 10, 26, "15: OH Resync")
window.printBox(26, 10, 26, "16: OH BC0")
window.printBox(52, 10, 26, "17: OH LV1A and Calpulse")
window.printBox(0, 11, 26, "19: OH trigger source")
window.printBox(26, 11, 26, "19: OH SBit select")
window.printBox(52, 11, 26, "20: OH VFAT2 clk source")
window.printBox(0, 12, 26, "21: OH VFAT2 clk fallback")
window.printBox(26, 12, 26, "22: OH CDCE clk source")
window.printBox(52, 12, 26, "23: OH CDCE clk fallback")
window.printBox(0, 13, 26, "24: OH ext LV1A cnt rst")
window.printBox(26, 13, 26, "25: OH int LV1A cnt rst")
window.printBox(52, 13, 26, "26: OH del LV1A cnt rst")
window.printBox(0, 14, 26, "27: OH LV1A cnt rst")
window.printBox(26, 14, 26, "28: OH int Cal cnt rst")
window.printBox(52, 14, 26, "29: OH del Cal cnt rst")
window.printBox(0, 15, 26, "30: OH Cal cnt rst")
window.printBox(26, 15, 26, "31: OH Resync cnt rst")
window.printBox(52, 15, 26, "32: OH BC0 cnt rst")
regId = window.inputInt(4, "Register address [0-32]:", 2, 0, 32, 0)

# Set the value
regValue = window.inputInt(17, "Register value [0-2^32]:", 10, 0, 500000, 0)

window.printLine(19, "Press [s] to apply the changes.", "Info", "center")
window.waitForKey("s")

# Change the register
if (regId == 0):
    glib.set("glib_reset_error_counter", regValue)
elif (regId == 1):
    glib.set("glib_reset_vfat2_rx_counter", regValue)
elif (regId == 2):
    glib.set("glib_reset_vfat2_tx_counter", regValue)
elif (regId == 3):
    glib.set("glib_reset_reg_rx_counter", regValue)
elif (regId == 4):
    glib.set("glib_reset_reg_tx_counter", regValue)
elif (regId == 5):
    glib.set("glib_empty_tracking_data", regValue)
elif (regId == 6):
    glib.set("glib_empty_trigger_data", regValue)
elif (regId == 7):
    glib.set("glib_sbit_select", regValue)
elif (regId == 8):
    glib.set("oh_reset_error_counter", regValue)
elif (regId == 9):
    glib.set("oh_reset_vfat2_rx_counter", regValue)
elif (regId == 10):
    glib.set("oh_reset_vfat2_tx_counter", regValue)
elif (regId == 11):
    glib.set("oh_reset_reg_rx_counter", regValue)
elif (regId == 12):
    glib.set("oh_reset_reg_tx_counter", regValue)
elif (regId == 13):
    glib.set("oh_lv1a", regValue)
elif (regId == 14):
    glib.set("oh_calpulse", regValue)
elif (regId == 15):
    glib.set("oh_resync", regValue)
elif (regId == 16):
    glib.set("oh_bc0", regValue)
elif (regId == 17):
    glib.set("oh_lv1a_and_calpulse", regValue)
elif (regId == 18):
    glib.set("oh_trigger_source", regValue)
elif (regId == 19):
    glib.set("oh_sbit_select", regValue)
elif (regId == 20):
    glib.set("oh_vfat2_src_select", regValue)
elif (regId == 21):
    glib.set("oh_vfat2_fallback", regValue)
elif (regId == 22):
    glib.set("oh_cdce_src_select", regValue)
elif (regId == 23):
    glib.set("oh_cdce_fallback", regValue)
elif (regId == 24):
    glib.set("oh_reset_ext_lv1a_counter", regValue)
elif (regId == 25):
    glib.set("oh_reset_int_lv1a_counter", regValue)
elif (regId == 26):
    glib.set("oh_reset_del_lv1a_counter", regValue)
elif (regId == 27):
    glib.set("oh_reset_lv1a_counter", regValue)
elif (regId == 28):
    glib.set("oh_reset_int_calpulse_counter", regValue)
elif (regId == 29):
    glib.set("oh_reset_del_calpulse_counter", regValue)
elif (regId == 30):
    glib.set("oh_reset_calpulse_counter", regValue)
elif (regId == 31):
    glib.set("oh_reset_resync_counter", regValue)
elif (regId == 32):
    glib.set("oh_reset_bc0_counter", regValue)

# Success
window.printLine(20, "Value written!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
