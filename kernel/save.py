import os, time, struct

class Save():

    path = ""
    f = False

    #####################################
    #   Open and close the file         #
    #####################################

    def __init__(self, folder):
        #self.path = os.path.dirname(os.path.abspath(__file__)) + "../..//test-beam-data/" + folder + "/" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
        self.path = "/opt/gemdaq/test-beam-data/" + folder + "/" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
        #moved back to test-beam-data###make the directory
        #moved back to test-beam-data#directory = "/tmp/" +folder
        #moved back to test-beam-data#if not os.path.exists(directory):
        #moved back to test-beam-data#    os.makedirs(directory)
        #moved back to test-beam-data#self.path = "/tmp/" +folder + "/" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
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
        self.f.write(struct.pack(">I", i))

    #####################################
    #   Helpers                         #
    #####################################

    def writePair(self, x, y):
        self.f.write(str(x)+"\t"+str(y)+"\n")

    def writeList(self, l):
        listValuesStr = ""
        for value in l:
            listValuesStr += str(value) + "\t"

        self.f.write(listValuesStr[:-1] + "\n")

    def writeDict(self, dictionnary):
        for key in dictionnary:
            self.write(str(key)+"\t"+str(dictionnary[key])+"\n")
