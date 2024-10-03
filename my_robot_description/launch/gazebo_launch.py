import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import TimerAction
import subprocess


def generate_launch_description():

    # 获取文件路径
    xacro_file = os.path.join(
        get_package_share_directory("my_robot_description"),
        "urdf",
        "xacro",
        "gazebo",
        "my_robot_base_gazebo.xacro",
    )
    # 定义临时 URDF 文件的路径
    urdf_file = os.path.join(
        get_package_share_directory("my_robot_description"),
        "urdf",
        "xacro",
        "gazebo",
        "my_robot_base_gazebo.urdf",
    )
    world_file = os.path.join(
        get_package_share_directory("my_robot_description"), "world", "2023_v_4_1.world"
    )
    if not os.path.exists(world_file):
        print(f"World file does not exist: {world_file}")
    try:
        subprocess.check_call(
            ["xacro", "--inorder", xacro_file], stdout=open(urdf_file, "w")
        )
    except subprocess.CalledProcessError as e:
        print(f"Error converting Xacro to URDF: {e}")
        return LaunchDescription([])

    return LaunchDescription(
        [
            ExecuteProcess(
                cmd=[
                    "/usr/bin/gzserver",
                    "--verbose",
                    "-s",
                    "libgazebo_ros_factory.so",
                    "-w",
                    world_file,
                ],
                output="screen",
            ),
            ExecuteProcess(cmd=["/usr/bin/gzclient"], output="screen"),
            TimerAction(
                period=5.0,  # 等待 5 秒确保 Gazebo 启动
                actions=[
                    Node(
                        package="gazebo_ros",
                        executable="spawn_entity.py",
                        output="screen",
                        arguments=[
                            "-file",
                            urdf_file,
                            "-entity",
                            "my_robot",
                        ],
                    ),
                ],
            ),
        ]
    )
