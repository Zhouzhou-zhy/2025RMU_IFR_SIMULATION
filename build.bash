#!/bin/bash

# 定义构建和安装的输出目录
BUILD_DIR="/home/zhy/zhy-ros2/build"
INSTALL_DIR="/home/zhy/zhy-ros2/install"

# 确保构建目录存在
mkdir -p "${BUILD_DIR}"
mkdir -p "${INSTALL_DIR}"

# 使用colcon在当前工作空间中构建指定的包
colcon build \
  --build-base "${BUILD_DIR}" \
  --install-base "${INSTALL_DIR}" \
  --symlink-install \
  --packages-select "my_robot_description" \
  
slam_gmapping_path="slam_gmapping"
colcon build \
    --base-paths "${slam_gmapping_path}" \
    --build-base "${BUILD_DIR}" \
    --install-base "${INSTALL_DIR}" \
    --symlink-install \
    --packages-select  openslam_gmapping slam_gmapping 

  

# 打印构建和安装完成的信息
echo "Build and installation completed."