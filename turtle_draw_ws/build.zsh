#!/bin/zsh

# Source zshrc to get micromamba function
source ~/.zshrc 2>/dev/null

# Activate ros_env
micromamba activate ros_env

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
