#!/bin/bash

# Runner for Turtle Draw
# Sets up PATH and sources ROS environment properly

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE="$SCRIPT_DIR/turtle_draw_ws"
ROS_ENV_PATH="${HOME}/.local/share/mamba/envs/ros_env"

# Add ROS bin to PATH first
export PATH="$ROS_ENV_PATH/bin:$PATH"
export PYTHONPATH="$ROS_ENV_PATH/lib/python3.10/site-packages:$PYTHONPATH"

# Source the workspace setup
source "$WORKSPACE/install/local_setup.bash" 2>/dev/null

# Run turtle drawer
ros2 run turtle_draw_pkg turtle_drawer
