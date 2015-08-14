import curses, sys, signal, time, math

class Window():

    window = False
    colors = dict()

    #####################################
    #   Open and close the Window       #
    #####################################

    # Initialize the Curses window
    def __init__(self, title):
        # Initialize the cursor mode
        self.window = curses.initscr()
        # Enable colors
        curses.start_color()
        curses.use_default_colors()
        # Disable keyboard input echo
        curses.noecho()
        # Do not require Enter to be pressed to get data
        curses.cbreak()
        # Hide cursor
        curses.curs_set(0)
        # Let Curses handle special keys
        # self.window.keypad(1)
        # Set signal for terminal resize
        signal.signal(signal.SIGWINCH, self.resizeSignal)
        # Set signal for exit
        signal.signal(signal.SIGINT, self.quitSignal)
        # Define basic colors
        self.defineColor("Default", 0, -1)
        self.defineColor("Title", 231, 0)
        self.defineColor("Subtitle", 231, 9)
        self.defineColor("Highlight", 0, 7)
        self.defineColor("Info", 231, 12)
        self.defineColor("Error", 231, 1)
        self.defineColor("Warning", 231, 3)
        self.defineColor("Success", 231, 2)
        self.defineColor("Input", 0, 11)
        self.defineColor("InputWait", 231, 5)
        self.defineColor("Options", 231, 4)
        # Draw the title
        self.printLine(0, title.upper(), "Title", "center")

    # Close the curses window
    def close(self):
        # End Curses
        curses.nocbreak()
        self.window.keypad(0)
        curses.echo()
        curses.endwin()

    # Go to non-blocking mode
    def disableBlocking(self):
        self.window.nodelay(1)

    # Go to block mode
    def enableBlocking(self):
        self.window.nodelay(0)


    #####################################
    #   Handle signals                  #
    #####################################

    # Resize signal
    def resizeSignal(self, signal, frame):
        # Refresh window
        self.window.refresh()

    # Quit signal
    def quitSignal(self, signal, frame):
        # Close window
        self.close()
        # Exit program
        sys.exit(0)

    #####################################
    #   Define colors                   #
    #####################################

    # Define colors
    def defineColor(self, name, text, back):
        # Define the color
        curses.init_pair(len(self.colors), text, back)
        # Save the color
        self.colors[name] = len(self.colors)

    #####################################
    #   Basic tool to print a string    #
    #####################################

    # Print a string on the screen
    def printString(self, x, y, string, color = "Default"):
        # Avoid going outside the terminal
        height, width = self.window.getmaxyx()
        if (y >= height): y = height - 1
        if (y == height - 1 and (x + len(string)) >= width - 1): string = string[:(width-x-1)]

        # Print the string
        self.window.addstr(y, x, string, curses.color_pair(self.colors[color]))
        # Refresh window
        self.window.refresh()

    #####################################
    #   Print a box of set size         #
    #####################################

    # Print a box of text
    def printBox(self, x, y, width, string, color = "Default", aligned = "left"):
        # Enlarge the string
        if (aligned == "left"): text = string + (" " * (width - len(string)))
        elif (aligned == "center"): text = (" " * int(math.floor((width - len(string)) / 2.))) + string + (" " * int(math.ceil((width - len(string)) / 2.)))
        elif (aligned == "right"): text = (" " * (width - len(string))) + string
        # Print the string
        self.printString(x, y, text, color)

    # Print a box of text
    def printLabel(self, x, y, width, string, value, color = "Default"):
        text = string + " " + (" " * (width - len(string) - len(str(value)) - 1)) + str(value)
        self.printString(x, y, text, color)

    #####################################
    #   Print a full line               #
    #####################################

    # Print a full line on the screen (auto-fill)
    def printLine(self, y, string, color = "Default", aligned = "left"):
        # Get the screen size
        height, width = self.window.getmaxyx()
        #
        if (y < 0): y = height + y
        # Print the string
        self.printBox(0, y, width, string, color, aligned)

    # Clear the screen (except title)
    def clear(self, fromY = 1, toY = 0):
        height, width = self.window.getmaxyx()
        toY = height - toY
        for i in range(fromY, toY): self.printLine(i, "")

    # Clear the screen (except title)
    def clearLine(self, y):
        self.printLine(y, "")


    #####################################
    #   Print an info and quit         #
    #####################################

    # Print info
    def printInfo(self, string):
        # Get the screen size
        height, width = self.window.getmaxyx()
        # Print the string
        self.printString(0, height - 4, string, "Info")
        #
        time.sleep(0.5)
        #
        self.printString(0, height - 4, (" " * len(string)))



    #####################################
    #   Print an error and quit         #
    #####################################

    # Print error
    def throwError(self, string):
        # Get the screen size
        height, width = self.window.getmaxyx()
        # Print the string
        self.printString(0, height - 2, string, "Error")
        #
        time.sleep(0.5)
        #
        self.printString(0, height - 2, (" " * len(string)))



    #####################################
    #   Basic input functions           #
    #####################################

    # Compare a char to what we get
    def getChr(self):
        return self.window.getch()

    # Get a character
    def getChar(self, x, y):
        # Enable echo mode
        curses.echo()
        # Get string
        while(True):
            # Mask previous text
            self.printBox(x, y, 1, " ", "Default")
            # Get text
            string = self.window.getstr(y, x, 1)
            if (string.isalnum() or len(string) == 0): break
        # Disable echo mode
        curses.noecho()
        # Return string
        return False if (len(string) == 0) else string

    # Get a string
    def getString(self, x, y, length = 50):
        # Enable echo mode
        curses.echo()
        # Get string
        while(True):
            # Mask previous text
            self.printBox(x, y, length, " ", "Default")
            # Get text
            string = self.window.getstr(y, x, length)
            if (string.isalnum() or len(string) == 0): break
        # Disable echo mode
        curses.noecho()
        # Return string
        return False if (len(string) == 0) else string

    # Get an integer
    def getInt(self, x, y, length = 50, placeholder = " "):
        # Enable echo mode
        curses.echo()
        # Get string
        while(True):
            # Mask previous text
            self.printBox(x, y, length, str(placeholder), "InputWait")
            # Get text
            string = self.window.getstr(y, x, length)
            if (string.isdigit() or len(string) == 0): break
        # Disable echo mode
        curses.noecho()
        # Return string
        return -1 if (len(string) == 0) else int(string)

    #####################################
    #   Advanced input functions        #
    #####################################

    # Helper to print a text box
    def inputInt(self, y, label, size = 3, minValue = 0, maxValue = 255, defaultValue = 0):
        return self.inputIntShifted(0, y, label, size, minValue, maxValue, defaultValue)

    def inputIntShifted(self, x, y, label, size = 3, minValue = 0, maxValue = 255, defaultValue = 0):
        labelLength = len(label) + 1
        self.printBox(x, y, labelLength, label, "Default", "left")
        inputData = self.getInt(x + labelLength, y, size, defaultValue)
        value = defaultValue if (inputData < minValue or inputData > maxValue) else inputData
        self.printBox(x + labelLength, y, size, str(value), "Input", "left")
        return value

    #####################################
    #   Wait functions                  #
    #####################################

    # Wait for a specific key signal
    def waitForKey(self, key):
        #
        self.enableBlocking()
        # Wait for key
        while (True):
            if (self.window.getch() == ord(key)): return True

    # Wait for quit signal
    def waitForQuit(self):
        # Get the screen size
        height, width = self.window.getmaxyx()
        # Print the string
        self.printLine(height - 1, "Press [q] to quit the program.", "Warning", "center")
        # Wait for key
        self.waitForKey('q')




    def drawColor(self):
        height, width = self.window.getmaxyx()
        for i in range(0, curses.COLORS):
            if (i != 0 and i % 60 == 0): self.window.getstr(0, 0, 1)
            self.defineColor(str(i), -1, i)
            self.printLine(i % 60, str(i), str(i))

