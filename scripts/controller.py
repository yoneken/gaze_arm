#!/usr/bin/python
# -*- coding:utf-8 -*-

import roslib; roslib.load_manifest('gaze_arm')
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from ros_gpio.srv import *


angles = [0., 0.]
gazebo_joint1 = None
gazebo_joint2 = None

def callback(msg):
  global angles
  angles[0] = angles[0] + msg.linear.x/10.0
  angles[1] = angles[1] + msg.angular.z/10.0

  if angles[0] < -1.57:
    angles[0] = -1.57
  if 1.57 < angles[0]:
    angles[0] = 1.57
  if angles[1] < -1.57:
    angles[1] = -1.57
  if 1.57 < angles[1]:
    angles[1] = 1.57

  rospy.loginfo("Angles %f, %f" % (angles[0], angles[1]))

  global gazebo_joint1, gazebo_joint2
  gazebo_joint1.publish(angles[0])
  gazebo_joint2.publish(angles[1])

  write_pwm = rospy.ServiceProxy("/write_pwm", WritePwm)
  write_pwm(5, 1.5/20.0 - angles[0]/3.1415*3.*0.5/20.0)
  write_pwm(6, 1.5/20.0 + angles[1]/3.1415*3.*0.5/20.0)

def controller():
  rospy.init_node("controller")

  global gazebo_joint1, gazebo_joint2
  gazebo_joint1 = rospy.Publisher('/gaze_arm/tip_joint_position_controller1/command', Float64, queue_size=100)
  gazebo_joint2 = rospy.Publisher('/gaze_arm/tip_joint_position_controller2/command', Float64, queue_size=100)

  initPWM()

  rospy.Subscriber("/cmd_vel", Twist, callback)
  rospy.spin()

  endPWM()

def initPWM():
  rospy.wait_for_service("/open_pwm")
  open_pwm = rospy.ServiceProxy("/open_pwm", OpenPwm)
  open_pwm(5)
  open_pwm(6)
  set_pwm_period = rospy.ServiceProxy("/set_pwm_period", SetPwmPeriod)
  set_pwm_period(5, 20000 * 20000/21800)
  set_pwm_period(6, 20000 * 20000/21800)
  start_pwm = rospy.ServiceProxy("/start_pwm", StartPwm)
  start_pwm(5)
  start_pwm(6)

def endPWM():
  stop_pwm = rospy.ServiceProxy("/stop_pwm", StopPwm)
  stop_pwm(5)
  stop_pwm(6)
  close_pwm = rospy.ServiceProxy("/close_pwm", CLosePwm)
  close_pwm(5)
  close_pwm(6)

if __name__ == "__main__":
  try:
    controller()
  except rospy.ROSInterruptException:
    pass
