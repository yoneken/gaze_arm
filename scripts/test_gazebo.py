#!/usr/bin/python
# -*- coding:utf-8 -*-

import roslib; roslib.load_manifest('gaze_arm')
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
#from ros_gpio.msg import GpioState


angles = [0., 0.]
proxy1 = None
proxy2 = None

def callback(msg):
  global angles
  angles[0] = angles[0] + msg.linear.x
  angles[1] = angles[1] + msg.angular.z
  rospy.loginfo("Angles %f, %f" % (angles[0], angles[1]))

  proxy1.publish(angles[0])
  proxy2.publish(angles[1])

def controller():
  rospy.init_node("controller")
  rospy.Subscriber("/cmd_vel", Twist, callback)
  rospy.spin()

if __name__ == "__main__":
  try:
    proxy1 = rospy.Publisher('/gaze_arm/tip_joint_position_controller1/command', Float64, queue_size=10)
    proxy2 = rospy.Publisher('/gaze_arm/tip_joint_position_controller2/command', Float64, queue_size=10)
    controller()
  except rospy.ROSInterruptException:
    pass
