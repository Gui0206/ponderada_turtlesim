# Turtle Draw: Drawing with Robot from Image Contours

A complete computer vision pipeline and ROS 2 package that extracts image contours and commands a turtle robot to draw them in the turtlesim simulator.

## Features

- **Custom Vision Pipeline**: Image preprocessing, edge detection, and contour extraction implemented from scratch using NumPy
- **Gaussian Blur**: Custom implementation using separable convolution
- **Sobel Edge Detection**: 2D convolution-based edge detection from scratch
- **Contour Extraction**: Connected component labeling and tracing
- **ROS 2 Integration**: Complete package with geometry message support
- **Coordinate Mapping**: Automatic image-to-turtle coordinate space transformation

## Implementation Details

### 1. Image Preprocessing

**Grayscale Conversion**: Standard luminosity formula applied to BGR image
- Formula: `Gray = 0.114*R + 0.587*G + 0.299*B`

**Gaussian Blur**: Separable 2D convolution using 1D Gaussian kernels
- Kernel size: 5x5
- Sigma: 1.5
- Approach: Horizontal then vertical 1D convolutions (more efficient)
- Boundary handling: Edge mode padding

### 2. Edge Detection

**Sobel Operator**: Implemented from scratch with 2D convolution
- Uses standard Sobel kernels (Sx, Sy)
- Magnitude calculation: `√(Gx² + Gy²)`
- Threshold: 50 (binary edge map)

**Why Sobel?**: 
- Robust to noise with built-in smoothing
- Directional gradient information
- Computationally efficient
- Well-suited for contour extraction

### 3. Contour Extraction

**Algorithm**: Flood fill with 8-connectivity
- Identifies connected components in edge maps
- Traces boundary pixels using depth-first search
- Minimum length filter to remove noise

**Coordinate Mapping**: Transforms image pixels to turtle coordinate space
- Normalizes to [0,1] space
- Maps to turtle bounds (0.5-10.5 in both axes)
- Inverts Y-axis (image top = turtle top)

### 4. Turtle Control

**ROS 2 Node**: Publishes velocity commands to `/turtle1/cmd_vel`
- Linear speed: 0.5 m/s
- Angular speed: 0.5 rad/s
- Movement accuracy: ±0.05 units
- Angle normalization: [-π, π]

## Project Structure

```
turtle_draw_pkg/
├── turtle_draw_pkg/
│   ├── __init__.py
│   ├── vision_pipeline.py      # Core vision processing
│   ├── turtle_drawer.py        # ROS 2 turtle control node
│   └── image_processor.py      # Visualization utility
├── package.xml                  # ROS 2 package metadata
├── setup.py                     # Python package setup
└── README.md                    # This file
```

## Installation

### Prerequisites

- ROS 2 (Humble or newer)
- Python 3.10+
- micromamba (as specified in requirements)

### Setup Steps

1. **Activate ROS environment**:
   ```bash
   micromamba activate ros_env
   ```

2. **Clone/navigate to workspace**:
   ```bash
   cd ~/Desktop/ponderada_ros/turtle_draw_ws
   ```

3. **Build the package**:
   ```bash
   colcon build
   ```

4. **Source the setup**:
   ```bash
   source install/setup.bash
   ```

## Running

### Start Turtlesim

In terminal 1:
```bash
micromamba activate ros_env
ros2 run turtlesim turtlesim_node
```

### Run Turtle Drawer

In terminal 2:
```bash
micromamba activate ros_env
cd ~/Desktop/ponderada_ros/turtle_draw_ws
source install/setup.bash
ros2 run turtle_draw_pkg turtle_drawer
```

The program will:
1. Load `dog.png` from the Desktop
2. Extract contours using the vision pipeline
3. Command the turtle to draw them

### Visualize Pipeline

To see the vision processing steps:
```bash
ros2 run turtle_draw_pkg image_processor
```

This generates `vision_pipeline_visualization.png` showing all processing stages.

## Algorithm Validation

### Testing Image Processing

The pipeline correctly handles:
- RGB to grayscale conversion with proper coefficients
- Gaussian blur preserves image structure while reducing noise
- Sobel edge detection identifies object boundaries
- Contour extraction traces meaningful shapes
- Coordinate mapping preserves aspect ratio and contour shape

### Performance Notes

- **Image size**: Works well with ~400x400 to 1000x1000 pixel images
- **Contour density**: Reduced to ~100-150 points per contour for smooth turtle movement
- **Processing time**: ~2-3 seconds for typical images
- **Drawing time**: ~10-30 seconds depending on contour complexity

## Implementation Choices & Justification

### Why Manual Convolution?

While slower than optimized libraries, manual implementation:
- Demonstrates understanding of fundamental algorithms
- Enables transparent algorithm visualization
- Allows fine-grained control over parameters
- Shows complete pipeline from first principles

### Why Sobel Over Canny?

- **Sobel**: Simpler to implement, sufficient for clear contours
- **Canny**: Would require non-maximal suppression and hysteresis thresholding (more complex)
- **Trade-off**: Slightly noisier edges but acceptable for robot drawing

### Contour Tracing Approach

**Flood Fill vs. Border Following**:
- **Selected**: Flood fill with connected components
- **Reason**: More robust to noise and broken edges
- **Alternative**: Could use Moore-Neighbor tracing for simpler contours

### Coordinate Mapping

Transforms image coordinates to turtle space:
- Scales proportionally (aspect ratio preserved)
- Centers within turtle bounds for visibility
- Inverts Y-axis (image standard vs. geometric)

## Dependencies

**Allowed by Requirements**:
- ✅ NumPy (matrix operations)
- ✅ OpenCV (image loading only)
- ✅ Matplotlib (visualization)

**Not Used** (as per requirements):
- ❌ scikit-image
- ❌ scipy
- ❌ PIL/Pillow (except OpenCV for loading)

## Known Limitations

1. **Complex Images**: Very cluttered images may produce many small contours
2. **Thin Objects**: Objects thinner than ~3 pixels may not be detected
3. **Movement Granularity**: 0.05 unit movement threshold; adjust for more precision
4. **Speed**: Manual convolution is slower than optimized C++ code

## Troubleshooting

### No contours detected
- Increase Sobel threshold (decrease from 50)
- Check image contrast
- Try different Gaussian blur parameters

### Turtle moves erratically
- Reduce linear/angular speed
- Increase movement threshold
- Check ROS clock sync

### Build errors
- Ensure ROS 2 is sourced: `source /opt/ros/humble/setup.bash`
- Rebuild: `colcon build --symlink-install`

## References

- ROS 2 Documentation: https://docs.ros.org/
- Sobel Operator: https://en.wikipedia.org/wiki/Sobel_operator
- Gaussian Blur: https://en.wikipedia.org/wiki/Gaussian_blur
- Connected Components: https://en.wikipedia.org/wiki/Connected-component_labeling
