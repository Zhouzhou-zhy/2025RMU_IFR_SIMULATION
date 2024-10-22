cmake_minimum_required(VERSION 3.5)
project(my_robot_description)

# 查找必要的包
find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)
find_package(xacro REQUIRED)

# 安装 xacro 文件
install(DIRECTORY urdf/
  DESTINATION share/${PROJECT_NAME}/urdf
)
# 安装URDF文件中的install文件夹
install(DIRECTORY
     launch/
  DESTINATION share/${PROJECT_NAME}/launch
)
# 安装 world 文件夹
install(DIRECTORY world/
  DESTINATION share/${PROJECT_NAME}/world
)
install(DIRECTORY meshes/
  DESTINATION share/${PROJECT_NAME}/meshes
)
install(DIRECTORY maps/
  DESTINATION share/${PROJECT_NAME}/maps
)
install(DIRECTORY config/
  DESTINATION share/${PROJECT_NAME}/config
)
# ament 包设置
ament_package()
