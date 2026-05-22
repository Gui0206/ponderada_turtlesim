"""
ROS 2 node that draws image contours using the turtle.
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

        # Turtle state
        self.position_x = 5.544445514 / 2  # Center approximately
        self.position_y = 5.544445514 / 2
        self.heading = 0.0  # Radians, 0 = facing right

        # Turtle speed parameters
        self.linear_speed = 0.5  # m/s
        self.angular_speed = 0.5  # rad/s

        # Turtle bounds (approximately)
        self.turtle_bounds = (0.5, 10.5, 0.5, 10.5)

        self.get_logger().info(f"Turtle Drawer initialized with image: {self.image_path}")

    def process_image(self):
        """Process image to extract contours."""
        self.get_logger().info("Processing image...")

        processor = ImageProcessor()
        processor.load_image(self.image_path)
        processor.to_grayscale()
        processor.preprocess()

        # Extract contours with reasonable density
        contours = processor.extract_contours(min_length=10)

        if not contours:
            self.get_logger().error("No contours found in image!")
            return []

        self.get_logger().info(f"Found {len(contours)} contours, filtering...")

        # Keep only the largest contours (most important)
        contours_by_size = sorted(contours, key=len, reverse=True)
        # Use top 5-10 contours for cleaner drawing
        max_contours = min(10, len(contours_by_size))
        significant_contours = contours_by_size[:max_contours]

        self.get_logger().info(f"Drawing top {len(significant_contours)} contours")

        # Map contours to turtle coordinate space
        mapper = CoordinateMapper(
            processor.original.shape,
            self.turtle_bounds
        )

        mapped_contours = []
        for contour in significant_contours:
            # Sample the contour to reduce points
            skeleton = processor.get_contour_skeleton(contour, max_points=100)
            mapped = mapper.map_contour(skeleton)
            mapped_contours.append(mapped)

        return mapped_contours

    def draw_contours(self, contours: list):
        """Draw the contours by commanding the turtle."""
        if not contours:
            self.get_logger().warn("No contours to draw")
            return

        self.get_logger().info(f"Drawing {len(contours)} contours...")

        # For each contour
        for contour_idx, contour in enumerate(contours):
            self.get_logger().info(f"Drawing contour {contour_idx + 1}/{len(contours)}")

            # Move to first point
            if len(contour) > 0:
                first_point = contour[0]
                self.move_to_point(first_point[0], first_point[1])

                # Draw the contour
                for point in contour[1:]:
                    self.draw_line_to(point[0], point[1])

            # Small pause between contours
            time.sleep(0.5)

        self.get_logger().info("Drawing complete!")

    def move_to_point(self, target_x: float, target_y: float):
        """Move turtle to a specific point."""
        # Clamp coordinates to valid bounds
        target_x = max(0.5, min(10.5, target_x))
        target_y = max(0.5, min(10.5, target_y))

        # Calculate distance and angle
        dx = target_x - self.position_x
        dy = target_y - self.position_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < 0.05:
            return

        target_angle = math.atan2(dy, dx)

        # Rotate to face target
        angle_diff = self._normalize_angle(target_angle - self.heading)
        self._rotate(angle_diff)

        # Move forward
        self._move_forward(distance)

        # Update position and heading
        self.position_x = target_x
        self.position_y = target_y
        self.heading = target_angle

    def draw_line_to(self, target_x: float, target_y: float):
        """Draw a line to target point."""
        # Clamp coordinates to valid bounds
        target_x = max(0.5, min(10.5, target_x))
        target_y = max(0.5, min(10.5, target_y))

        dx = target_x - self.position_x
        dy = target_y - self.position_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < 0.05:
            return

        target_angle = math.atan2(dy, dx)

        # Rotate
        angle_diff = self._normalize_angle(target_angle - self.heading)
        self._rotate(angle_diff)

        # Move (line is drawn automatically as turtle moves)
        self._move_forward(distance)

        self.position_x = target_x
        self.position_y = target_y
        self.heading = target_angle

    def _move_forward(self, distance: float):
        """Move turtle forward."""
        twist = Twist()
        twist.linear.x = self.linear_speed if distance > 0 else -self.linear_speed
        distance = abs(distance)

        # Calculate time to travel
        time_to_travel = distance / self.linear_speed
        end_time = time.time() + time_to_travel

        while time.time() < end_time:
            self.velocity_publisher.publish(twist)
            time.sleep(0.01)

        # Stop
        twist.linear.x = 0.0
        self.velocity_publisher.publish(twist)
        time.sleep(0.05)

    def _rotate(self, angle: float):
        """Rotate turtle by given angle (radians)."""
        if abs(angle) < 0.01:
            return

        twist = Twist()
        twist.angular.z = self.angular_speed if angle > 0 else -self.angular_speed
        angle = abs(angle)

        # Calculate time to rotate
        time_to_rotate = angle / self.angular_speed
        end_time = time.time() + time_to_rotate

        while time.time() < end_time:
            self.velocity_publisher.publish(twist)
            time.sleep(0.01)

        # Stop
        twist.angular.z = 0.0
        self.velocity_publisher.publish(twist)
        time.sleep(0.05)

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
        # Process image
        contours = drawer.process_image()

        # Draw the contours
        drawer.draw_contours(contours)

    except Exception as e:
        drawer.get_logger().error(f"Error: {str(e)}")
    finally:
        drawer.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
