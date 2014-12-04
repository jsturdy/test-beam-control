import os, time, struct

class Save():

    path = ""
    f = False

    #####################################
    #   Open and close the file         #
    #####################################

    def __init__(self, folder):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/../../test-beam-data/" + folder + "/" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
        self.f = open(self.path, "w", 0)
        self.f.write("Time\t" + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n")

    def switchToBinary(self):
        self.close()
        self.f = open(self.path, "ab", 0)

    def close(self):
        self.f.close()

    #####################################
    #   Basic write functions           #
    #####################################

    def write(self, string):
        self.f.write(str(string))

    def writeLine(self, string):
        self.f.write(str(string) + "\n")

    def writeInt(self, i):
        self.f.write(struct.pack("I", i))

    #####################################
    #   Helpers                         #
    #####################################

    def writePair(self, x, y):
        self.f.write(str(x)+"\t"+str(y)+"\n")

    def writeDict(self, dictionnary):
        for key in dictionnary:
            self.write(str(key)+"\t"+str(dictionnary[key])+"\n")

    def writeEvent(self, bc, ec, chipid, data1, data2, data3, data4, crc, bx):
        self.writeInt(bc)
        self.write('\t')
        self.writeInt(ec)
        self.write('\t')
        self.writeInt(chipid)
        self.write('\t')
        self.writeInt(data1)
        self.write('\t')
        self.writeInt(data2)
        self.write('\t')
        self.writeInt(data3)
        self.write('\t')
        self.writeInt(data4)
        self.write('\t')
        self.writeInt(crc)
        self.write('\t')
        self.writeInt(bx)
        self.write('\n')

