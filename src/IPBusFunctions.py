import sys, os, time, signal, random

# Get IPBus
ipbus_path = os.path.dirname(os.path.abspath(__file__)) + "/src"
sys.path.append(ipbus_path)
from PyChipsUser import *

#
class GLIB:

    ipbus = False

    # Create IPBus
    def __init__(self, ipaddress, table):
        ipbusAddrTable = AddressTable(table)
        self.ipbus = ChipsBusUdp(ipbusAddrTable, ipaddress, 50001)

    # Read operation
    def get(self, register):
        for i in range(0, 5):
            try:
                controlChar = self.ipbus.read(register)
                return controlChar
            except ChipsException, e:
                pass
        return False

    # Write operation
    def set(self, register, value):
        for i in range(0, 5):
            try:
                self.ipbus.write(register, value)
                return True
            except ChipsException, e:
                pass
        return False

