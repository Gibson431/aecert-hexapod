alias sb="source ~/.bash_aliases"
alias cw="cd ~/ros2_ws"

sr () {
    source "/opt/ros/${ROS_DISTRO}/setup.bash"
    source "${HOME}/ros2_ws/install/setup.bash"
};

cb  () {
    cw
    colcon build
    sr
};

cb
sr

export GAZEBO_RESOURCE_PATH=$GAZEBO_RESOURCE_PATH:$HOME/ros2_ws/src/robotic-control-practice
export GAZEBO_PLUGIN_PATH=$GAZEBO_PLUGIN_PATH:$HOME/ros2_ws/install