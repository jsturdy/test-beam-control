import os, time

testBeamDataPath = os.path.dirname(os.path.abspath(__file__)) + "/../../../test-beam-data/"

class Save():

    f = False

    #####################################
    #   Open and close the file         #
    #####################################

    def __init__(self, folder):
        fileName = os.path.dirname(os.path.abspath(__file__)) + "/../../../test-beam-data/" + folder + "/" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
        self.f = open(fileName, "w", 0)
        self.f.write("Time;" + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n")

    def close(self):
        self.f.close()

    #####################################
    #   Basic write functions           #
    #####################################

    def write(self, string):
        self.f.write(str(string))

    def writeLine(self, string):
        self.f.write(str(string) + "\n")

    #####################################
    #   Helpers                         #
    #####################################

    def writePair(self, x, y):
        self.f.write(str(x)+";"+str(y)+"\n")

    def writeDict(self, dictionnary):
        for key in dictionnary:
            self.write(str(key)+";"+str(dictionnary[key])+"\n")

