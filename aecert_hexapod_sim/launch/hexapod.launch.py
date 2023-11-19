import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration, ThisLaunchFileDir
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Get the directories of Turtlebot3 packages
    hex_description_dir = get_package_share_directory('aecert_hexapod_description')
    hex_gazebo_dir = get_package_share_directory('aecert_hexapod_sim')

    # Declare the launch arguments
    model_arg = DeclareLaunchArgument(
        'model',
        default_value='burger',
        description='Model type: burger, waffle, or waffle_pi'
    )

    # Set the robot description
    robot_description = {
        'robot_description': Command([
            'xacro ', os.path.join(hex_description_dir, 'urdf', 'hexapod', '.urdf.xacro')
        ])
    }

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=['-entity', 'hexapod', '-topic', 'robot_description'],
        output='screen'
    )

    # Include Turtlebot3 control launch file
    # control_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([hex_gazebo_dir, '/launch', '/turtlebot3_control.launch.py'])
    # )

    # Create and return the launch description
    ld = LaunchDescription([
        model_arg,
        SetEnvironmentVariable('GAZEBO_MODEL_PATH', os.path.join(hex_description_dir, 'models')),
        spawn_entity,
        # control_launch
    ])

    return ld
