import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import TimerAction

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=['/usr/bin/gzserver', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),
        ExecuteProcess(
            cmd=['/usr/bin/gzclient'],
            output='screen'
        ),
        TimerAction(
            period=5.0,  # 等待 5 秒确保 Gazebo 启动
            actions=[
                Node(
                    package='gazebo_ros',
                    executable='spawn_entity.py',
                    output='screen',
                    arguments=[
                        '-file',
                        os.path.join(get_package_share_directory('my_robot_description'), 'urdf', 'xacro', 'gazebo', 'my_robot_base_gazebo.urdf'),
                        '-entity', 'my_robot',
                        '-x','0',
                        '-y','0',
                        '-z','5'
                    ]
                )
            ]
        )
    ])
