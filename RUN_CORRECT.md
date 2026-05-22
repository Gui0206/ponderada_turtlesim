# Correct Way to Run

The issue is that the ROS environment setup needs to be done **in your current shell**, not in a subprocess.

## ✅ CORRECT METHOD

### Terminal 1: Start Turtlesim

```bash
source ~/.zshrc
micromamba activate ros_env
ros2 run turtlesim turtlesim_node
```

### Terminal 2: Run Turtle Drawer

```bash
source ~/.zshrc
micromamba activate ros_env
cd ~/Desktop/ponderada_ros/turtle_draw_ws
source install/setup.bash
ros2 run turtle_draw_pkg turtle_drawer
```

---

## ⚠️ Why Scripts Don't Work

The setup.bash script tries to source files from the ROS environment, which requires your shell to be properly initialized with all the ROS environment variables.

When you run `bash RUN.sh` or `zsh RUN.sh`, it creates a **new subprocess** with a fresh environment, so the ROS setup doesn't work properly.

---

## ✅ Alternative: Use This Instead

If you want a one-liner that works, run this in your shell first:

```bash
source ~/.zshrc && \
micromamba activate ros_env && \
cd ~/Desktop/ponderada_ros/turtle_draw_ws && \
source install/setup.bash && \
ros2 run turtle_draw_pkg turtle_drawer
```

---

## Summary

**DO THIS:**
1. Activate ROS in your current terminal
2. Source setup.bash in the workspace
3. Run ros2 commands

**NOT THIS:**
- Don't try to run setup scripts as subprocess (bash RUN.sh)
- They need to run in your current shell context
