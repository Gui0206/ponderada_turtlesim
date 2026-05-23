#!/bin/bash

# Build and setup Turtle Draw ROS 2 package

echo "========================================="
echo "Turtle Draw - Build Script"
echo "========================================="

# Activate ROS environment
echo "Activating ROS environment..."
eval "$(micromamba shell hook --shell bash)"
micromamba activate ros_env

# Navigate to workspace
cd "$(dirname "$0")"

echo ""
echo "Building package..."
colcon build

echo ""
echo "Sourcing install scripts..."
source install/setup.bash

echo ""
echo "========================================="
echo "Build complete!"
echo ""
echo "To use in this terminal, run:"
echo "  source install/setup.bash"
echo ""
echo "Then start turtlesim (in another terminal):"
echo "  ros2 run turtlesim turtlesim_node"
echo ""
echo "Test the vision pipeline:"
echo "  cd src/turtle_draw_pkg"
echo "  python3 create_test_image.py"
echo "  ros2 run turtle_draw_pkg vision_pipeline test_shapes.png"
echo ""
echo "Or draw with the turtle:"
echo "  ros2 run turtle_draw_pkg turtle_drawer test_shapes.png"
echo "========================================="
