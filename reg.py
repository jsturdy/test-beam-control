#!/bin/env python

from kernel import *

import uhal

#from optparse import OptionParser
#parser = OptionParser()
#parser.add_option("-s", "--slot", type="int", dest="slot",
#		  help="slot in uTCA crate", metavar="slot", default=4)
#
#parser.add_option("-o", "--links", type="string", dest="activeLinks", action='append',
#		  help="pair of connected optical links (GLIB,OH)", metavar="activeLinks", default=[])
#(options, args) = parser.parse_args()
#
#links = {}
#for link in options.activeLinks:
#	pair = map(int, link.split(","))
#	links[pair[0]] = pair[1]
#print "links", links
#
uhal.setLogLevelTo( uhal.LogLevel.FATAL )

#glib = GLIB(2,{0:0, 1:1, 2:2})
glib = GLIB(4,{1:1})
#glib = GLIB()

if (sys.argv[1] == 'w' and len(sys.argv) == 4):
    print "Write to ", sys.argv[2]
    glib.set(sys.argv[2], int(sys.argv[3]))
elif (sys.argv[1] == 'r' and len(sys.argv) == 3):
    print "Read from ", sys.argv[2], " : ", hex(glib.get(sys.argv[2]))
else:
    print "Nothing to do..."




