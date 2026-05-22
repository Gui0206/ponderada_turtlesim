#!/bin/zsh

echo "╔═══════════════════════════════════════════════════════╗"
echo "║   TURTLE DRAW - Quickstart Guide                      ║"
echo "║   Robotic Drawing from Image Contours                 ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Source zshrc to activate micromamba
source ~/.zshrc 2>/dev/null

# Activate ROS environment
echo "🔧 Activating ros_env..."
micromamba activate ros_env

cd "$(dirname "$0")" || exit 1
WORKSPACE="$(pwd)/turtle_draw_ws"

echo "📂 Workspace: $WORKSPACE"
echo ""

# Check if already built
if [ ! -d "$WORKSPACE/install" ]; then
    echo "🔨 Building ROS 2 package..."
    zsh "$WORKSPACE/build.zsh" || exit 1
    echo "✅ Build complete!"
    echo ""
else
    echo "✅ Package already built"
    echo ""
fi

# Source setup
echo "📦 Sourcing setup.bash..."
source "$WORKSPACE/install/setup.bash"

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║  INSTRUCTIONS                                         ║"
echo "╠═══════════════════════════════════════════════════════╣"
echo "║                                                       ║"
echo "║  TERMINAL 1 (Turtlesim):                             ║"
echo "║  $ micromamba activate ros_env                       ║"
echo "║  $ ros2 run turtlesim turtlesim_node                 ║"
echo "║                                                       ║"
echo "║  TERMINAL 2 (Turtle Drawer):                         ║"
echo "║  $ micromamba activate ros_env                       ║"
echo "║  $ cd ~/Desktop/ponderada_ros/turtle_draw_ws         ║"
echo "║  $ source install/setup.bash                         ║"
echo "║  $ ros2 run turtle_draw_pkg turtle_drawer            ║"
echo "║                                                       ║"
echo "║  (Optional) Visualize pipeline:                      ║"
echo "║  $ ros2 run turtle_draw_pkg image_processor          ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "Press ENTER to continue, or close this terminal."
echo ""
read -p "Ready? (Enter) "

echo "🚀 Launching ROS 2 Turtle Drawer..."
echo ""
echo "Make sure turtlesim is running in another terminal!"
echo ""
ros2 run turtle_draw_pkg turtle_drawer
