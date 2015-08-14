#!/bin/env python

import sys, os, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/kernel")
from ipbus import *

####################################################

print
print "This python script will test the GLIB, optical links, OH, and VFAT2 functionalities."
print "Simply follow the instructions on the screen in order to diagnose the setup."
print "Thomas Lenzi - tlenzi@ulb.ac.be"
print

####################################################

Passed = '\033[92m' + "Passed... " + '\033[0m'
Failed = '\033[91m' + "Failed... " + '\033[0m' 

def txtTitle(str):
    print '\033[1m' + str + '\033[0m'

####################################################

txtTitle("A. Testing the GLIB")
print 

glibIP = raw_input("Enter the GLIB's IP address: ")
print 

# glibIP = "192.168.0.161"
glib = GLIB(glibIP.strip())

# Read GLIB firmware

data = glib.get("glib_firmware_version")
if (data == 0):
    print "Test " + Failed + "could not read the GLIB firmware version"
    print
    sys.exit()
else:
    print "Test " + Passed + "the GLIB firmware version is: " + hex(data)

print

####################################################

txtTitle("B. Testing the Optical Links")
print 

data0 = glib.get("oh_firmware_version_0")
data1 = glib.get("oh_firmware_version_1")
data2 = glib.get("oh_firmware_version_2")

v01 = (data0 == data1)
v02 = (data0 == data2)
v12 = (data1 == data2)

links = [True, True, True]

if (v01 and v02):
    print "Test " + Passed + "link 0 is working"
    print "Test " + Passed + "link 1 is working"
    print "Test " + Passed + "link 2 is working"
else:
    if (v01 and not v12):
        print "Test " + Passed + "link 0 is working"
        print "Test " + Passed + "link 1 is working"
        print "Test " + Failed + "link 2 is not working"
        links[2] = False
    elif (v02 and not v12):
        print "Test " + Passed + "link 0 is working"
        print "Test " + Failed + "link 1 is not working"
        print "Test " + Passed + "link 2 is working"
        links[1] = False
    elif (v12 and not v01):
        print "Test " + Failed + "link 0 is not working"
        print "Test " + Passed + "link 1 is working"
        print "Test " + Passed + "link 2 is working"
        links[0] = False
    else:
        print "Test " + Failed + "more than one link is not working"

print

####################################################

txtTitle("C. Detecting the VFAT2s over I2C")
print 

presentVFAT2s = []

for i in range(0, 24):
    if (links[i / 8]):
        data = glib.get("vfat2_" + str(i) + "_chipid0")
        error = (data >> 26) & 0x1
        valid = (data >> 25) & 0x1
        data = data & 0xff 

        if (error):
            print "#" + str(i) + "\t" + Failed + "not detected"
        else:
            if (data == 0):
                print "#" + str(i) + "\t" + Failed + "bad data (possibly due to no pull-ups)"
            elif (valid):
                print "#" + str(i) + "\t" + Passed + "present"
                presentVFAT2s.append(i)
            else:
                print "#" + str(i) + "\t" + Failed + "unknown error"
    else:
        print "#" + str(i) + "\t" + Failed + "link not present"

print
print "Detected " + str(len(presentVFAT2s)) + " VFAT2s: " + str(presentVFAT2s)
print

####################################################

txtTitle("D. Testing the I2C communication with the VFAT2s")
print 
print "Test: performing 10 random write/read operations for each present VFAT2"
print 

for i in presentVFAT2s:
    validOperations = 0
    for j in range(0, 10):
        writeData = random.randint(0, 255)
        glib.set("vfat2_" + str(i) + "_ctrl3", writeData)
        readData = glib.get("vfat2_" + str(i) + "_ctrl3") & 0xff
        if (readData == writeData):
            validOperations += 1
    glib.set("vfat2_" + str(i) + "_ctrl3", 0)
    if (validOperations == 10):
        print "#" + str(i) + "\t" + Passed + "all operations succeed"
    else:
        print "#" + str(i) + "\t" + Failed + "only " + str(validOperations) + " / 10 operations were successful"

print

####################################################

txtTitle("E. Reading out tracking data")
print
print "Test: sending triggers and testing if the Event Counter adds up"
print 

glib.set("oh_trigger_source", 2)

for i in presentVFAT2s:
    glib.set("vfat2_" + str(i) + "_ctrl0", 0)
    glib.set("vfat2_" + str(i) + "_ctrl0", 55)
    glib.set("glib_empty_tracking_data_" + str(i / 8), 1)

    packet1 = packet2 = packet3 = packet4 = packet5 = packet6 = packet7 = 0

    nPackets = 0
    nLV1As = 0
    ecs = []

    while (nPackets < 10):
        if (glib.get("glib_track_" + str(i / 8) + "_req") == 0x1): 
            packet6 = glib.get("glib_track_" + str(i / 8) + "_d6")
            ec = int((0x00000ff0 & packet6) >> 4)
            nPackets += 1
            ecs.append(ec)
        else:
            nLV1As += 1
            glib.set("oh_lv1a", 1)
        if (nLV1As == 1000):
            break

    glib.set("vfat2_" + str(i) + "_ctrl0", 0)

    if (nPackets != 10):
        print "#" + str(i) + "\t" + Failed + "only receive " + str(nPackets) + " / 10 data packets: " + str(ecs)
    else:
        followingECS = True
        for j in range(0, 9):
            if (ecs[j + 1] - ecs[j] != 1):
                followingECS = False
        if (followingECS):
            print "#" + str(i) + "\t" + Passed + "the EC add up: " + str(ecs)
        else:
            print "#" + str(i) + "\t" + Failed + "the EC do not add up: " + str(ecs)

print 





