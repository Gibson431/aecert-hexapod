FROM osrf/ros:iron-desktop-full

# Add vscode user with same UID and GID as your host system
# (copied from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
# Switch from root to user
USER $USERNAME

# Add user to video group to allow access to webcam
RUN sudo usermod --append --groups video $USERNAME

# Update all packages
RUN sudo apt update && sudo apt upgrade -y

# Install Git
RUN sudo apt install -y git

# Customise the installation
USER root

RUN apt-get update -y && apt-get install -y \
    python3 \
    python3-yaml \
    python3-rospkg \
    python3-pip

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN apt-get update && apt-get install -y \
    wget \
    x11-apps

# RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' \
#     && wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - \
#     && apt-get update -y \
#     && apt-get install -y gazebo11 \
#     && apt install -y ros-${ROS_DISTRO}-gazebo-ros-pkgs

# RUN sudo apt update && sudo apt-get install -y \
#     ros-${ROS_DISTRO}-demo-nodes-cpp

RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-ros2-control \
    ros-${ROS_DISTRO}-ros2-controllers \
    ros-${ROS_DISTRO}-gz-ros2-control

USER $USERNAME

# RUN pip install defusedxml
RUN mkdir -p /home/$USERNAME/ros_ws/src

# Rosdep update
RUN rosdep update

# Source the ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc