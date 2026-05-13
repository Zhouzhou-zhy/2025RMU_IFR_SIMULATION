# my_robot

RMU IFR 仿真平台：提供小车模型、Gazebo 仿真环境以及 SLAM Gmapping 建图功能。

## 项目结构

```
├── my_robot_description/    # 机器人模型与仿真环境
│   ├── launch/              # Gazebo 仿真启动文件
│   ├── config/              # Nav2 导航参数
│   ├── maps/                # RMU 场地地图
│   ├── urdf/xacro/          # 机器人 URDF/Xacro 模型
│   ├── world/               # Gazebo 世界文件
│   └── meshes/              # 模型网格文件
├── slam_gmapping/           # SLAM Gmapping 建图
│   ├── openslam_gmapping/   # OpenSlam Gmapping 核心 C++ 库
│   └── slam_gmapping/       # ROS2 封装节点（发布 /map 话题）
└── build.bash               # 一键构建脚本
```

## 环境要求

- **ROS2 Foxy**（基于 ament_cmake 构建）
- **Gazebo Classic**（`gzserver` + `gzclient` 位于 `/usr/bin/`）
- `colcon` 构建工具
- 依赖包：`urdf`、`xacro`、`tf2`、`tf2_ros`、`tf2_geometry_msgs`、`nav_msgs`、`sensor_msgs`、`message_filters`、`turtlebot3_navigation2`

## 构建

```bash
bash build.bash
```

构建脚本按顺序编译两个阶段：

1. 先编译 `my_robot_description`
2. 再编译 `openslam_gmapping` 和 `slam_gmapping`

> **注意**：`build.bash` 中的 `BUILD_DIR` 和 `INSTALL_DIR` 默认为 `/home/zhy/zhy-ros2/build` 和 `/home/zhy/zhy-ros2/install`，请根据实际环境修改。构建使用了 `--symlink-install`，因此修改 launch/config/urdf 文件后无需重新编译即可生效。

## 启动

### 启动 Gazebo 仿真

```bash
ros2 launch my_robot_description gazebo_launch.py
```

该命令会依次启动：

- Gazebo 服务器（加载 RMU 场地世界）
- 5 秒延迟后加载机器人模型、robot_state_publisher 和 Nav2 导航

### 启动 SLAM 建图

```bash
ros2 launch slam_gmapping slam_gmapping.launch.py
```

SLAM 节点订阅 `/scan`（`sensor_msgs/LaserScan`），发布 `/map`（`nav_msgs/OccupancyGrid`），同时发布 `/map_metadata` 和 `/entropy`。需要确保 TF 变换正常可用。

## 关键文件

| 文件                                                         | 说明                   |
| ------------------------------------------------------------ | ---------------------- |
| `build.bash`                                                 | colcon 一键构建脚本    |
| `my_robot_description/launch/gazebo_launch.py`               | Gazebo + Nav2 仿真启动 |
| `my_robot_description/config/navigation.yaml`                | Nav2 导航参数配置      |
| `my_robot_description/maps/7v7map.yaml`                      | RMU 场地导航地图       |
| `my_robot_description/world/2023_v_4_1.world`                | Gazebo 世界文件        |
| `slam_gmapping/slam_gmapping/launch/slam_gmapping.launch.py` | SLAM 节点启动          |
| `AGENTS.md`                                                  | AI Agent 开发辅助说明  |

## 常见问题

1. **Gazebo 启动失败**：确认已安装 Gazebo Classic（非 Ignition/Garden），`gzserver` 和 `gzclient` 路径正确。
2. **地图路径错误**：`gazebo_launch.py` 中地图路径硬编码为 `/home/zhy/zhy-ros2/my_robot/my_robot_description/maps/7v7map.yaml`，需改为实际路径。
3. **缺少 turtlebot3_navigation2**：Nav2 导航依赖该外部包，请确保已安装。
