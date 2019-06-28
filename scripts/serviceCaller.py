#!/usr/bin/env python

import sys
import argparse
import numpy as np
import rospy
import time
import socket

from sensor_msgs.msg import LaserScan
from sick_safetyscanners.msg import FieldMsg
from sick_safetyscanners.srv import FieldData

# Parse Arguments
myargv = rospy.myargv(argv=sys.argv)
parser = argparse.ArgumentParser(description='help function')
parser.add_argument('-s', action='store_true', help='Set if you get data from laser scanner - if false the programm will wait for data to be published on /laserTopic')
parser.add_argument('-n', type=int, default=0, help='Number of protective field to show')
parser.add_argument('--ip', type=str, default='192.168.43.105', help='IP Address of HoloLens')
args = parser.parse_args(myargv[1:])
TCP_IP = args.ip

# Check if we get data from Laser Scanner or externally
if args.s:
    print("Getting data from Laserscanner - Field {0}".format(args.n))
    rospy.wait_for_service('/sick_safetyscanners/field_data')
    serviceCall = rospy.ServiceProxy('/sick_safetyscanners/field_data', FieldData)
    field_list = serviceCall()
    field = field_list.fields[args.n]
else:
    print('Waiting for topic')
    field = rospy.wait_for_message('/laserTopic',FieldMsg, timeout=30)

# Convert the range values to manageable sizes
l=[]
x=np.array_split(field.ranges,27)
for j in x:
    l.append(max(j))
values=",".join('{0:.5}'.format(e) for e in l)

values = values + ''.join('0' for i in range(0, 200))
#print(values)

#rospy.Publisher('/laserTopic',FieldMsg, queue_size=3)

# Callback function
def callback(ScanObj, TCP_IP):
    TCP_PORT = 9090
    BUFFER_SIZE = 200
    MESSAGE = str(ScanObj) #.SerializeToString()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    print(data)
    s.close()

# now send the values every 5s
while True:
    #values=",".join('{0:.5}'.format(np.random.random_sample()*3) for e in l)
    #values = values + ''.join('0' for i in range(0, 200))
    print(len(values),values)
    callback(values,TCP_IP)
    print('alive')
    time.sleep(10)
