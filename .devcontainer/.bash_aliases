alias sb="source ~/.bash_aliases"
alias cw="cd ~/ros_ws"

sr () {
    source "/opt/ros/${ROS_DISTRO}/setup.bash"
    source "${HOME}/ros_ws/install/setup.bash"
};

cb  () {
    cw
    colcon build
    sr
};

cb