# System imports
from kernel import *

# Create window
window = Window("Empty the trigger data buffer")

# Get GLIB access
glib = GLIB()
glib.setWindow(window)

# Design
window.printLine(4, "Press [s] to empty the trigger data buffer.", "Info", "center")
window.waitForKey("s")

# Empty the buffers
glib.set("glib_empty_trigger_data", 0)

# Log the changes
save = Save("log")
save.writeLine("Trigger data buffer emptied")
save.close()

# Design
window.printLine(5, "Trigger buffers emptied!", "Success", "center")

# Wait before quiting
window.waitForQuit()

# Close window
window.close()
