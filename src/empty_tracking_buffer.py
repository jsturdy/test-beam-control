# System imports
from system import *

# Create window
window = Window("Empty the tracking data buffer")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Design
window.printLine(4, "Press [s] to empty the tracking data buffer.", "Info", "center")
window.waitForKey("s")

# Empty the buffers
glib.set('glib_empty_tracking_data', 0)

# Log the changes
save = Save("log")
save.writeLine("Tracking data buffer emptied")
save.close()

# Design
window.printLine(5, "Tracking buffers emptied!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
