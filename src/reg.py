from kernel import *

glib = GLIB()

if (sys.argv[1] == 'w' and len(sys.argv) >= 4):
    print "Write to ", sys.argv[2]
    glib.write(sys.argv[2], int(sys.argv[3]))
elif (sys.argv[1] == 'r' and len(sys.argv) >= 3):
    print "Read from ", sys.argv[2], " : ", hex(glib.read(sys.argv[2]))
else:
    print "Nothing can be done..."



