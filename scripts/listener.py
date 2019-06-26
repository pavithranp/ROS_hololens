#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import socket

TCP_IP = '192.168.43.105'
TCP_PORT = 9090
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
    print(data.data)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()

def parse_data(data):
    #parse the messages
    return data.data
    

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('/sick_safetyscanners/scan',LaserScan, callback)


    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
