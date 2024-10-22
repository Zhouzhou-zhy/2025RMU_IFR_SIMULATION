import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess,IncludeLaunchDescription, SetEnvironmentVariable
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import TimerAction
import subprocess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():


#xacro_file_3V3=os.path.join(get_package_share_directory())
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
    
    navigation2_launch_file = os.path.join(
        get_package_share_directory('turtlebot3_navigation2'),
        'launch',
        'navigation2.launch.py'
    )
    navigation2_launch = IncludeLaunchDescription(
                            PythonLaunchDescriptionSource(navigation2_launch_file),
                            launch_arguments={
                                'use_sim_time': 'true',
                                 'map': '/home/zhy/zhy-ros2/my_robot/my_robot_description/maps/7v7map.yaml'
                            }.items()
                        )

    return LaunchDescription(
        [
             SetEnvironmentVariable('TURTLEBOT3_MODEL', 'waffle'),
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
                            "-x", "7",  # 设置初始位置的 x 坐标
                            "-y", "4",  # 设置初始位置的 y 坐标
                            "-z", "0",  # 设置初始位置的 z 坐标
                        ],
                    ),

                    Node(
                        package="robot_state_publisher",
                        executable="robot_state_publisher",
                        name="robot_state_publisher",
                        output="screen",
                        parameters=[
                            {"robot_description": open(urdf_file).read()}
                        ],  # 加载 URDF 文件内容
                    ),
                    # 包含 `navigation2.launch.py` 文件并传递参数
                    #   Node(
                    #         package='nav2_controller',
                    #         executable='controller_server',
                    #         parameters=[
                    #                         PathJoinSubstitution(
                    #                             [get_package_share_directory('my_robot_description'), 'config', 'navigation.yaml']
                    #                         )
                    #                      ],
                    #         output='screen',
                    #         ),
                     navigation2_launch,
                ],
            ),
        
    
        ]
    )
