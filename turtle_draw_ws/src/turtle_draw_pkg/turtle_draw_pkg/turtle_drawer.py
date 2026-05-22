"""
ROS 2 node that draws image contours using the turtle.
Simple, fast, and respects turtlesim bounds properly.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import math
import numpy as np
from turtle_draw_pkg.vision_pipeline import ImageProcessor, CoordinateMapper


class TurtleDrawer(Node):
    """ROS 2 node for controlling turtle to draw image contours."""

    def __init__(self, image_path: str = None):
        super().__init__('turtle_drawer')

        self.velocity_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.image_path = image_path or '/Users/guilhermeholanda/Desktop/ponderada_ros/dog.png'

        # Turtle state (start at center of turtlesim 11x11 space)
        self.position_x = 5.5
        self.position_y = 5.5
        self.heading = 0.0  # Radians, 0 = facing right

        # FAST turtle speeds
        self.linear_speed = 2.0  # m/s - much faster
        self.angular_speed = 2.0  # rad/s - much faster

        # Turtlesim bounds: 0.0 to 11.0
        self.x_min, self.x_max = 0.0, 11.0
        self.y_min, self.y_max = 0.0, 11.0

        self.get_logger().info(f"Turtle Drawer initialized")
        self.get_logger().info(f"Bounds: X=[{self.x_min}, {self.x_max}], Y=[{self.y_min}, {self.y_max}]")

    def process_image(self):
        """Process image to extract the main contour."""
        self.get_logger().info("Processing image...")

        processor = ImageProcessor()
        processor.load_image(self.image_path)
        processor.to_grayscale()
        processor.preprocess()

        # Extract contours
        all_contours = processor.extract_contours(min_length=20)

        if not all_contours:
            self.get_logger().error("No contours found!")
            return []

        # Get ONLY the largest contour (main dog shape)
        largest = max(all_contours, key=len)
        self.get_logger().info(f"Using largest contour: {len(largest)} points")

        # Map to turtle space
        mapper = CoordinateMapper(
            processor.original.shape,
            (self.x_min, self.x_max, self.y_min, self.y_max)
        )

        # Sample points for smooth drawing
        skeleton = processor.get_contour_skeleton(largest, max_points=80)
        mapped = mapper.map_contour(skeleton)

        self.get_logger().info(f"Mapped to {len(mapped)} drawing points")
        return [mapped]

    def draw_contours(self, contours: list):
        """Draw contours efficiently."""
        if not contours:
            self.get_logger().warn("No contours to draw")
            return

        for contour_idx, contour in enumerate(contours):
            self.get_logger().info(f"Drawing contour {contour_idx + 1}")

            if len(contour) < 2:
                continue

            # Move to start (pen up)
            first_point = contour[0]
            self._move_direct(first_point[0], first_point[1])

            # Draw rest (pen down - turtle draws as it moves)
            for point in contour[1:]:
                self._draw_direct(point[0], point[1])

        self.get_logger().info("Drawing complete!")

    def _clamp(self, value: float, min_val: float, max_val: float) -> float:
        """Clamp value to range."""
        return max(min_val, min(max_val, value))

    def _move_direct(self, target_x: float, target_y: float):
        """Move directly to point (fast)."""
        # Ensure coordinates are within bounds
        target_x = self._clamp(target_x, self.x_min, self.x_max)
        target_y = self._clamp(target_y, self.y_min, self.y_max)

        # Simple direct movement
        self._go_to(target_x, target_y)

    def _draw_direct(self, target_x: float, target_y: float):
        """Draw line to point (fast)."""
        # Ensure coordinates are within bounds
        target_x = self._clamp(target_x, self.x_min, self.x_max)
        target_y = self._clamp(target_y, self.y_min, self.y_max)

        # Same as move (turtle draws as it moves)
        self._go_to(target_x, target_y)

    def _go_to(self, target_x: float, target_y: float):
        """Go to target position."""
        dx = target_x - self.position_x
        dy = target_y - self.position_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < 0.01:  # Already there
            return

        # Calculate target angle
        target_angle = math.atan2(dy, dx)
        angle_diff = self._normalize_angle(target_angle - self.heading)

        # Rotate if needed
        if abs(angle_diff) > 0.05:
            self._rotate_fast(angle_diff)

        # Move forward
        self._move_fast(distance)

        # Update state
        self.position_x = target_x
        self.position_y = target_y
        self.heading = target_angle

    def _move_fast(self, distance: float):
        """Move forward FAST."""
        if distance < 0.01:
            return

        twist = Twist()
        twist.linear.x = self.linear_speed if distance > 0 else -self.linear_speed
        distance = abs(distance)

        time_needed = distance / self.linear_speed
        end_time = time.time() + time_needed

        while time.time() < end_time:
            self.velocity_publisher.publish(twist)
            time.sleep(0.005)  # 5ms updates instead of 10ms

        twist.linear.x = 0.0
        self.velocity_publisher.publish(twist)
        time.sleep(0.01)

    def _rotate_fast(self, angle: float):
        """Rotate FAST."""
        if abs(angle) < 0.01:
            return

        twist = Twist()
        twist.angular.z = self.angular_speed if angle > 0 else -self.angular_speed
        angle = abs(angle)

        time_needed = angle / self.angular_speed
        end_time = time.time() + time_needed

        while time.time() < end_time:
            self.velocity_publisher.publish(twist)
            time.sleep(0.005)

        twist.angular.z = 0.0
        self.velocity_publisher.publish(twist)
        time.sleep(0.01)

    def _normalize_angle(self, angle: float) -> float:
        """Normalize angle to [-pi, pi]."""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle


def main(args=None):
    """Main ROS 2 entry point."""
    rclpy.init(args=args)

    drawer = TurtleDrawer()

    try:
        contours = drawer.process_image()
        drawer.draw_contours(contours)
    except Exception as e:
        drawer.get_logger().error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        drawer.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
