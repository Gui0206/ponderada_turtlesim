#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen
import numpy as np
import argparse
import time

from .image_processor import ImageProcessor


class TurtleDrawer(Node):
    """ROS 2 node that draws image contours using turtlesim with teleportation."""

    def __init__(self, image_path: str = None):
        super().__init__('turtle_drawer')

        self.image_path = image_path

        # Create service clients
        self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')

        # Wait for services
        while not self.teleport_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /turtle1/teleport_absolute service...')

        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /turtle1/set_pen service...')

        self.get_logger().info('Services ready! Starting to draw...')

    def extract_points_from_binary_image(self, binary_image: np.ndarray) -> list:
        """Extract all white pixels from binary image and map to turtle space."""
        height, width = binary_image.shape

        # Find all white pixels
        y_indices, x_indices = np.where(binary_image == 255)

        if len(x_indices) == 0:
            self.get_logger().warn('No white pixels found in image')
            return []

        # Map to turtle space with margins
        points = []
        margin = 0.5
        turtle_bounds = 11.0
        available_space = turtle_bounds - (2 * margin)

        min_x, max_x = np.min(x_indices), np.max(x_indices)
        min_y, max_y = np.min(y_indices), np.max(y_indices)

        # Calculate scale to fit in turtle space
        largest_dim = max(max_x - min_x, max_y - min_y)
        scale = available_space / (largest_dim + 1)

        for x, y in zip(x_indices, y_indices):
            # Map to turtle coordinates
            turtle_x = margin + (x - min_x) * scale
            turtle_y = margin + (max_y - y) * scale
            points.append((turtle_x, turtle_y))

        self.get_logger().info(f'Extracted {len(points)} points from image')
        return points

    def teleport_turtle(self, x: float, y: float, theta: float = 0.0):
        """Teleport turtle to position."""
        request = TeleportAbsolute.Request()
        request.x = x
        request.y = y
        request.theta = theta

        future = self.teleport_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def set_pen(self, r: int = 0, g: int = 0, b: int = 0, width: int = 1, off: int = 0):
        """Set pen properties (color, width, on/off)."""
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        future = self.pen_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def draw_image(self):
        """Main drawing function."""
        if self.image_path is None:
            self.get_logger().error('Image path not set')
            return False

        try:
            # Load image
            self.get_logger().info(f'Loading image: {self.image_path}')
            image = ImageProcessor.load_image(self.image_path)
            self.get_logger().info(f'Image shape: {image.shape}')

            # Preprocess
            self.get_logger().info('Preprocessing image...')
            binary = ImageProcessor.preprocess(image)

            # Extract points
            self.get_logger().info('Extracting points...')
            points = self.extract_points_from_binary_image(binary)

            if len(points) == 0:
                self.get_logger().warn('No points to draw')
                return False

            # Draw
            self.get_logger().info(f'Starting to draw {len(points)} points...')
            time.sleep(1.0)

            # Lift pen and move to first point
            self.set_pen(off=1)
            self.teleport_turtle(points[0][0], points[0][1])
            self.set_pen(off=0)

            # Draw all points
            jump_threshold = 0.3  # Distance threshold for jumping (lifting pen)

            for i, (x, y) in enumerate(points):
                if i > 0:
                    # Check distance to previous point
                    prev_x, prev_y = points[i - 1]
                    distance = np.sqrt((x - prev_x)**2 + (y - prev_y)**2)

                    if distance > jump_threshold:
                        # Jump: lift pen, teleport, lower pen
                        self.set_pen(off=1)
                        self.teleport_turtle(x, y)
                        self.set_pen(off=0)
                    else:
                        # Continue drawing
                        self.teleport_turtle(x, y)

                if (i + 1) % 100 == 0:
                    self.get_logger().info(f'Drawn {i + 1}/{len(points)} points')

            self.get_logger().info('Drawing complete!')
            return True

        except Exception as e:
            self.get_logger().error(f'Error: {str(e)}')
            import traceback
            traceback.print_exc()
            return False


def main(args=None):
    rclpy.init(args=args)

    parser = argparse.ArgumentParser(description='Turtle Draw - Draw image with turtlesim')
    parser.add_argument('image', nargs='?', help='Path to image file')
    args = parser.parse_args(args)

    if args.image is None:
        print('Usage: turtle_drawer <image_path>')
        print('Example: turtle_drawer /path/to/image.png')
        return

    node = TurtleDrawer(image_path=args.image)

    try:
        node.draw_image()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
