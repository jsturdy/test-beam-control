# System imports
import sys, time, select
from kernel import *

def wait():
    start_time = time.time()
    while (True):
        if (time.time() - start_time > 2): return False
        i, o, e = select.select([sys.stdin],[],[],0.0001)
        for s in i:
            if s == sys.stdin:
                inp = sys.stdin.readline()
                return inp

if (wait() != "aze\n"):
    print "You shouldn't use this script !"
    sys.exit(0)

glib = GLIB()

while (True):
    print "Values sets"

    glib.set("oh_trigger_source", 2)
    glib.set("oh_sbit_select", 4)
    glib.set("glib_sbit_select", 4)
    glib.set("oh_vfat2_src_select", 1)
    glib.set("oh_cdce_src_select", 1)
    glib.set("oh_vfat2_fallback", 0)
    glib.set("oh_cdce_fallback", 0)

    glib.setVFAT2(9, "ctrl0", 0)

    glib.setVFAT2(12, "ctrl0", 55)
    glib.setVFAT2(12, "ctrl1", 0)
    glib.setVFAT2(12, "ctrl2", 48)
    glib.setVFAT2(12, "ctrl3", 0)
    glib.setVFAT2(12, "ipreampin", 168)
    glib.setVFAT2(12, "ipreampfeed", 80)
    glib.setVFAT2(12, "ipreampout", 150)
    glib.setVFAT2(12, "ishaper", 150)
    glib.setVFAT2(12, "ishaperfeed", 100)
    glib.setVFAT2(12, "icomp", 75)
    glib.setVFAT2(12, "vthreshold1", 30)
    glib.setVFAT2(12, "vthreshold2", 0)
    glib.setVFAT2(12, "vcal", 0)
    glib.setVFAT2(12, "calphase", 0)
    glib.setVFAT2(12, "latency", 13)

    time.sleep(60)

