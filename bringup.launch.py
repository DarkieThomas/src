from launch import LaunchDescription
from launch.actions import ExecuteProcess

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os
import xacro


def generate_launch_description():

    pkg_path = get_package_share_directory('darkie')

    xacro_file = os.path.join(
        pkg_path,
        'urdf',
        'maze_urdf.xacro'
    )

    robot_description_config = xacro.process_file(xacro_file)

    robot_description = {
        'robot_description': robot_description_config.toxml()
    }

    controller_config = os.path.join(
        pkg_path,
        'config',
        'controllers.yaml'
    )

    return LaunchDescription([

        # robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[robot_description]
        ),

        # ros2_control
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[
                robot_description,
                controller_config
            ],
            output='screen'
        ),

        # joint_state_broadcaster
        ExecuteProcess(
            cmd=[
                'ros2',
                'control',
                'load_controller',
                '--set-state',
                'active',
                'joint_state_broadcaster'
            ],
            output='screen'
        ),

        # diff_drive_controller
        ExecuteProcess(
            cmd=[
                'ros2',
                'control',
                'load_controller',
                '--set-state',
                'active',
                'diff_drive_controller'
            ],
            output='screen'
        ),

    ])







//




from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os
import xacro


def generate_launch_description():

    pkg_path = get_package_share_directory('darkie')

    xacro_file = os.path.join(
        pkg_path,
        'urdf',
        'maze_urdf.xacro'
    )

    robot_description_config = xacro.process_file(xacro_file)

    robot_description = {
        'robot_description': robot_description_config.toxml()
    }

    controller_config = os.path.join(
        pkg_path,
        'config',
        'controllers.yaml'
    )

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[robot_description]
        ),

        Node(
            package='controller_manager',
            executable='ros2_control_node',
            output='screen',
            parameters=[controller_config]
        ),

        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster'],
            output='screen'
        ),

        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['diff_drive_controller'],
            output='screen'
        ),

