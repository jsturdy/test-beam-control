# System imports
from system import *
import time

# Get GLIB access
glib = GLIB()

for i in range(0, 1000):

    if (sys.argv[1] == 'w'):
        glib.set(sys.argv[2], int(sys.argv[3]))

    elif (sys.argv[1] == 'r'):
        glib.get(sys.argv[2])

    time.sleep(1)



