#!/bin/bash
set -e

# Activate ros_env
eval "$(micromamba shell hook --shell bash)"
micromamba activate ros_env

# Source ROS setup
# source /opt/ros/humble/setup.bash 2>/dev/null || true

# Build
cd "$(dirname "$0")"
echo "Building ROS 2 package..."
colcon build --symlink-install

echo ""
echo "Build complete!"
echo ""
echo "To use this package, run:"
echo "  source install/setup.bash"
echo "  ros2 run turtle_draw_pkg turtle_drawer"
