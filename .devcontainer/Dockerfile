FROM osrf/ros2:nightly

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

RUN sudo apt update && sudo apt-get install -y \
    ros-${ROS_DISTRO}-demo-nodes-cpp

USER $USERNAME

# RUN pip install defusedxml

# Rosdep update
RUN rosdep update

RUN mkdir -p /home/$USERNAME/ros2_ws/src

# Source the ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc