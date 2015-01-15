# Gaze Arm
Gaze Arm is a cheap robot arm controlled with [ROS](http://ros.org).
![Gaze Arm](https://pbs.twimg.com/media/B7RztmbCMAEsBRr.jpg)

# Hardware
- [GWS Micro 2BBMG - Micro Servo](http://www.servodatabase.com/servo/gws/micro-2bbmg) x2
- Servo bracket x2
- Smart phone holder
- USB webcam
- AC adapter
- [Intel Edison](http://www.intel.com/content/www/us/en/do-it-yourself/edison.html)
- PC (Ubuntu recommended)

# Software
- [ROS](http://ros.org)
- [Gazebo](gazebosim.org)
- [libmraa](https://github.com/intel-iot-devkit/mraa)
- [ros_gpio](https://github.com/yoneken/ros_gpio)

# Launch
**Both PC and Edison**

1. Install ROS (PC: Desktop-Full, Edison: Bare Bones), libmraa.
2. Add ros_gpio node.
  1. $ cd *ros_source_folder* 
  2. $ wstool set --git ros_gpio https://github.com/yoneken/ros_gpio.git
  3. $ wstool update ros_gpio

**on PC**

1. Install Gazebo.
2. Add gaze_arm node.
  1. $ cd *ros_source_folder* 
  2. $ wstool set --git gaze_arm https://github.com/yoneken/gaze_arm.git
  3. $ wstool update gaze_arm
3. Make nodes.
  1. $ make_catkin_isolated --install --pkg ros_gpio gaze_arm
4. Set ROS_MASTER_URI and ROS_IP. For example, IP address of your PC is XXX.XXX.XXX.XXX:
  1. $ export ROS_MASTER_URI="http://XXX.XXX.XXX.XXX:11311"
  2. $ export ROS_IP="XXX.XXX.XXX.XXX"
5. Set parmeter for gscam.
  1. $ export GSCAM_CONFIG="v4l2src device=/dev/video0 ! video/x-raw-rgb ! ffmpegcolorspace"
6. Launch gaze_arm node.
  1. $ roslaunch gaze_arm gaze_arm.launch

**on Edison**

1. Make ros_gpio node.
  1. $ make_catkin_isolated --install --pkg ros_gpio
2. Set ROS_MASTER_URI and ROS_IP. For example, IP address of your Edison is YYY.YYY.YYY.YYY:
  1. $ export ROS_MASTER_URI="http://XXX.XXX.XXX.XXX:11311"
  2. $ export ROS_IP="YYY.YYY.YYY.YYY"
3. Connect servo motors' signal pin to Edison's 5 and 6 pin.
4. Run ros_gpio node.
  1. $ rosrun ros_gpio srv_server

Now. You can control the arm to type "i", ",", "j", and "l" keys.
In gazeno, the simulation model is moved synchronously with the real robot.

# Arm structure
![Gaze Arm Structure](https://pbs.twimg.com/media/B7UYWZMCYAA3sZl.png)
