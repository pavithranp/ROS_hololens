#!/usr/bin/env python

import sys
import argparse

import rospy


from sensor_msgs.msg import LaserScan
from sick_safetyscanners.msg import FieldMsg
from sick_safetyscanners.srv import FieldData
import laserscan_pb2



myargv = rospy.myargv(argv=sys.argv)
parser = argparse.ArgumentParser(description='help.')
parser.add_argument('-s', action='store_true')
parser.add_argument('-n', type=int, default= 0)


args = parser.parse_args(myargv[1:])

if args.s:
    print("Getting data from Laserscanner - Field {0}".format(args.n))
    rospy.wait_for_service('/sick_safetyscanners/field_data')
    serviceCall = rospy.ServiceProxy('/sick_safetyscanners/field_data', FieldData)
    field_list = serviceCall()
    field = field_list.fields[args.n]
    l=[]
    x=np.array_split(field.ranges,27)
    for j in x:
        l.append(max(j))
    values=",".join(repr(e) for e in np.around(l,5))
else:
    print('Waiting for topic')
    field = rospy.wait_for_message('/laserTopic',FieldMsg, timeout=30)

ScanObject = laserscan_pb2.Laserscan()
ScanObject.angle_min = field.start_angle
ScanObject.angle_increment = field.angular_resolution
ScanObject.ranges.extend(field.ranges)

#print(field)
#print(len(ScanObject.SerializeToString()))
#import numpy as np
#print(np.array(field.ranges).max(),np.array(field.ranges).min())

import socket

def callback(ScanObj):
    #print('hi im a callback')
    TCP_IP = '192.168.43.105'
    TCP_PORT = 9090
    BUFFER_SIZE = 15000
    MESSAGE = str(ScanObj) #.SerializeToString()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    s.close()

import time
while True:

    callback(values)
    print('alive')
    time.sleep(5)
