# Quick Start - Turtle Draw

## ✅ Everything is Ready!

The project is fully built and tested. Follow these simple steps:

---

## 🚀 Run (2 Terminals Required)

### **Terminal 1: Start Turtlesim**

```bash
micromamba activate ros_env
ros2 run turtlesim turtlesim_node
```

A window with a turtle will appear. Leave this running.

### **Terminal 2: Run Turtle Drawer**

```bash
cd ~/Desktop/ponderada_ros
micromamba activate ros_env
zsh RUN.sh
```

The turtle will start drawing the dog contours! 🐕🎨

---

## 📊 Test the Vision Pipeline (No ROS Needed)

To see the image processing steps without running ROS:

```bash
micromamba activate ros_env
python3 ~/Desktop/ponderada_ros/test_vision_pipeline.py
```

Expected output:
```
✅ Image loaded: shape=(720, 1280, 3)
✅ Grayscale conversion
✅ Sobel edge detection
✅ Contour extraction: 178 contours found
✅ Visualization saved
```

---

## 🔧 If Setup.bash Has Issues

If you see errors about `local_setup.bash`, try this:

```bash
# Terminal setup
source ~/.zshrc
micromamba activate ros_env

# Navigate to workspace
cd ~/Desktop/ponderada_ros/turtle_draw_ws

# Source setup (use bash instead of zsh)
bash -c "source install/setup.bash && /bin/zsh"

# Now you can run
ros2 run turtle_draw_pkg turtle_drawer
```

Or just use the simpler runner:

```bash
zsh ~/Desktop/ponderada_ros/RUN.sh
```

---

## 📁 Project Files

- `README.md` - Full overview
- `RELATORIO.md` - Technical documentation
- `EXECUCAO.md` - Detailed execution guide
- `test_vision_pipeline.py` - Test script
- `RUN.sh` - Simple runner
- `turtle_draw_ws/` - ROS 2 package

---

## ✨ What You'll See

1. Turtlesim window opens with white turtle on gray background
2. Turtle starts drawing dog contours automatically
3. Takes ~20-30 seconds to complete
4. Drawing shows the main contours of the dog image

---

**Status**: ✅ READY TO RUN
