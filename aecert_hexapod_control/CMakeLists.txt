cmake_minimum_required(VERSION 3.5)
project(aecert_hexapod_control LANGUAGES CXX)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

################################################################################
# Install
################################################################################
install(TARGETS 
  ${EXEC_NAME}
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY 
  launch
  config
  DESTINATION share/${PROJECT_NAME}/
)

install(DIRECTORY 
  include/
  DESTINATION include/
)

# ament_export_targets(export_ros2_control_test_assets HAS_LIBRARY_TARGET)
ament_package()