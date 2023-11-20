import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
import xacro


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    # Package Directories
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    # pkg_ros_gz_sim_demos = get_package_share_directory('ros_gz_sim_demos')
    pkg_aecert_sim = get_package_share_directory('aecert_hexapod_sim')
    pkg_aecert_desc = get_package_share_directory('aecert_hexapod_description')

    # Parse robot description from xacro
    robot_description_file = os.path.join(pkg_aecert_desc, 'urdf', 'hexapod.urdf.xacro')
    robot_description_config = xacro.process_file(
        robot_description_file
    )
    robot_description = {'robot_description': robot_description_config.toxml()}

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
    )

    # Gazebo Sim
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments=[('gz_args', ['-r -v 4 empty.sdf'])]
    )

    # Spawn
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'aecert_hexapod',
            '-topic', 'robot_description',
        ],
        output='both',
    )

    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_trajectory_controller'],
        output='screen'
    )

    # Gz - ROS Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Clock (IGN -> ROS2)
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            # Joint states (IGN -> ROS2)
            '/world/empty/model/aecert_hexapod/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
        ],
        remappings=[
            ('/world/empty/model/aecert_hexapod/joint_state', 'joint_states'),
        ],
        output='screen'
    )

    delay_load_joint_state_broadcaster = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn,
            on_exit=[load_joint_state_broadcaster]
        )
    )

    delay_load_joint_trajectory_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=load_joint_state_broadcaster,
            on_exit=[load_joint_trajectory_controller]
        )
    )

    launch_args = DeclareLaunchArgument(
        'use_sim_time',
        default_value=use_sim_time,
        description='If true, use simulated clock'
    )

    nodes = [
        # Nodes and Launches
        gazebo,
        delay_load_joint_state_broadcaster,
        delay_load_joint_trajectory_controller,
        robot_state_publisher,
        spawn,
        launch_args
    ]

    return LaunchDescription(nodes)