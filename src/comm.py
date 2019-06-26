#!/usr/bin/env python

import socket
import roslib
import rospy
from sensor_msgs.msg import LaserScan
import laserscan_pb2
TCP_IP = '192.168.43.105'
TCP_PORT = 9090
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
x=laserscan_pb2.Laserscan()
rospy.Subscriber('/scan', LaserScan, self.process_scan)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
#data = s.recv(BUFFER_SIZE)
s.close()

print "message data:", MESSAGE
