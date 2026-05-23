#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
import argparse
import sys

from .image_processor import ImageProcessor
from .contour_extractor import ContourExtractor
from .path_planner import PathPlanner


class TurtleDrawer(Node):
    """ROS 2 node that draws image contours using turtlesim."""

    def __init__(self, image_path: str = None):
        super().__init__('turtle_drawer')

        self.image_path = image_path
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub_pose = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        self.current_pose = None
        self.drawing_complete = False

        # Parameters
        self.linear_speed = 2.0  # units/sec
        self.angular_speed = 1.0  # radians/sec
        self.position_tolerance = 0.05
        self.angle_tolerance = 0.01

        self.get_logger().info(f'TurtleDrawer initialized. Image: {image_path}')

    def pose_callback(self, msg: Pose):
        """Callback to receive turtle's current pose."""
        self.current_pose = msg

    def process_image_and_draw(self):
        """Main pipeline: process image and draw contours."""
        if self.image_path is None:
            self.get_logger().error('Image path not set')
            return False

        try:
            # Step 1: Load and preprocess image
            self.get_logger().info('Loading image...')
            image = ImageProcessor.load_image(self.image_path)

            self.get_logger().info(f'Image shape: {image.shape}')

            # Step 2: Preprocess
            self.get_logger().info('Preprocessing image...')
            binary = ImageProcessor.preprocess(image)

            # Step 3: Extract contours
            self.get_logger().info('Extracting contours...')
            contours = ContourExtractor.find_contours(binary)
            self.get_logger().info(f'Found {len(contours)} contours')

            # Filter and process contours
            contours = ContourExtractor.filter_contours_by_size(contours, min_size=10)
            self.get_logger().info(f'After filtering: {len(contours)} contours')

            if len(contours) == 0:
                self.get_logger().warn('No contours found in image')
                return False

            # Simplify contours
            simplified_contours = []
            for contour in contours:
                simplified = ContourExtractor.simplify_contour(contour, epsilon=3.0)
                if len(simplified) > 5:
                    simplified_contours.append(simplified)

            self.get_logger().info(f'After simplification: {len(simplified_contours)} contours')

            # Step 4: Plan paths
            self.get_logger().info('Planning paths...')
            planner = PathPlanner(image.shape)
            paths = planner.contours_to_paths(simplified_contours)

            self.get_logger().info(f'Planned {len(paths)} paths')

            # Step 5: Draw paths
            self.get_logger().info('Starting to draw...')
            time.sleep(2.0)  # Give turtle time to settle

            for path_idx, path in enumerate(paths):
                self.get_logger().info(f'Drawing path {path_idx + 1}/{len(paths)} ({len(path)} points)')

                # Move to start of path
                if len(path) > 0:
                    self.move_to(path[0][0], path[0][1])

                # Draw the path
                for i in range(1, len(path)):
                    target_x, target_y = path[i]
                    self.move_to(target_x, target_y)

                # Small pause between contours
                time.sleep(0.5)

            self.get_logger().info('Drawing complete!')
            self.drawing_complete = True
            return True

        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')
            import traceback
            traceback.print_exc()
            return False

    def move_to(self, target_x: float, target_y: float, timeout: float = 10.0):
        """Move turtle to target position."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.current_pose is None:
                self.get_logger().warn('Waiting for pose data...')
                time.sleep(0.1)
                continue

            # Calculate distance and angle to target
            dx = target_x - self.current_pose.x
            dy = target_y - self.current_pose.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < self.position_tolerance:
                # Reached target
                self.stop()
                return True

            target_angle = math.atan2(dy, dx)
            angle_diff = target_angle - self.current_pose.theta

            # Normalize angle to [-pi, pi]
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi

            # Create velocity command
            cmd = Twist()

            # If angle difference is large, rotate first
            if abs(angle_diff) > self.angle_tolerance:
                cmd.angular.z = self.angular_speed if angle_diff > 0 else -self.angular_speed
                cmd.linear.x = 0.0
            else:
                cmd.linear.x = min(self.linear_speed, distance)
                cmd.angular.z = 0.0

            self.pub.publish(cmd)
            time.sleep(0.05)

        self.get_logger().warn(f'Timeout moving to ({target_x}, {target_y})')
        self.stop()
        return False

    def stop(self):
        """Stop turtle movement."""
        cmd = Twist()
        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    parser = argparse.ArgumentParser(description='Turtle Draw - Draw image contours using turtlesim')
    parser.add_argument('image', nargs='?', help='Path to image file')
    args = parser.parse_args(args)

    if args.image is None:
        print('Usage: turtle_drawer <image_path>')
        print('Example: turtle_drawer /path/to/image.png')
        return

    node = TurtleDrawer(image_path=args.image)

    try:
        node.process_image_and_draw()
    finally:
        node.stop()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
