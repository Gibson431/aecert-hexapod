# aecert hexapod ros

A ROS2 controller for [Aecert Robotics](https://github.com/Ryan-Mirch/Aecerts_Hexapod_V1/tree/main)' hexapod.

THIS IS NOT AN OFFICIAL PACKAGE. IT IS AN INDEPENDENT PROJECT.

## Usage ##

### Dev Container ###

The dev container has been created to work with VSCode. It is required to be run on a linux system with X11 or XWayland installed. The container also needs access to the xhost.

Give access to the display protocol through:
```bash
xhost +
```
Warning, this is an insecure way of routing the Gazebo GUI, I have not bothered to figure out which hosts actually need access. Use at your own risk.

### Hardware ###

My current implementation involves a modified version of the official design that utilises a RaspberryPi Zero 2W as the brains.