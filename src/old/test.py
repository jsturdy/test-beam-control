# System imports
import time
from system import *

# Get GLIB access
glib = GLIB('192.168.0.115', 'register_mapping.dat')

for i in range(0, 300000):
    glib.set('oh_bc0', 0)
    time.sleep(0.1)
