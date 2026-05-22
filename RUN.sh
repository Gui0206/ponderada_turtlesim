#!/bin/zsh

# Simple runner that doesn't use interactive read (avoids zsh issues)

source ~/.zshrc 2>/dev/null

micromamba activate ros_env

cd "$(dirname "$0")" || exit 1
WORKSPACE="$(pwd)/turtle_draw_ws"

# Source the setup
source "$WORKSPACE/install/setup.bash" 2>/dev/null

# Run directly
ros2 run turtle_draw_pkg turtle_drawer
