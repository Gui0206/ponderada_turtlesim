import numpy as np
from typing import List, Tuple


class PathPlanner:
    """
    Convert image contours to turtle movement commands.
    Handles coordinate transformation and path planning.
    """

    def __init__(self, image_shape: Tuple[int, int], turtle_bounds: Tuple[float, float, float, float] = (0, 0, 11, 11)):
        """
        Initialize path planner.

        Args:
            image_shape: (height, width) of image
            turtle_bounds: (min_x, min_y, max_x, max_y) of turtle drawing area
        """
        self.image_height, self.image_width = image_shape
        self.turtle_min_x, self.turtle_min_y, self.turtle_max_x, self.turtle_max_y = turtle_bounds

    def contours_to_paths(self, contours: List[np.ndarray]) -> List[List[Tuple[float, float]]]:
        """
        Convert multiple contours to turtle paths.

        Args:
            contours: List of contours (each is array of (x, y) points)

        Returns:
            List of paths (each path is list of (x, y) coordinates in turtle space)
        """
        paths = []
        for contour in contours:
            path = self.contour_to_path(contour)
            if len(path) > 2:
                paths.append(path)
        return paths

    def contour_to_path(self, contour: np.ndarray) -> List[Tuple[float, float]]:
        """Convert single contour to turtle path."""
        path = []
        for point in contour:
            turtle_x, turtle_y = self.image_to_turtle_coords(point[0], point[1])
            path.append((turtle_x, turtle_y))
        return path

    def image_to_turtle_coords(self, img_x: float, img_y: float) -> Tuple[float, float]:
        """
        Transform image coordinates to turtle drawing space.

        Image coordinates: (0, 0) at top-left
        Turtle coordinates: (0, 0) at center of screen, x increases right, y increases up
        """
        # Scale from image space to turtle space
        turtle_x = (img_x / self.image_width) * (self.turtle_max_x - self.turtle_min_x) + self.turtle_min_x
        turtle_y = (img_y / self.image_height) * (self.turtle_max_y - self.turtle_min_y) + self.turtle_min_y

        # Flip y-axis and center (turtle center is 5.5, 5.5 by default)
        turtle_y = self.turtle_max_y - turtle_y + self.turtle_min_y

        return float(turtle_x), float(turtle_y)

    @staticmethod
    def calculate_angle(from_point: Tuple[float, float], to_point: Tuple[float, float]) -> float:
        """Calculate angle (in radians) from one point to another."""
        dx = to_point[0] - from_point[0]
        dy = to_point[1] - from_point[1]
        return np.arctan2(dy, dx)

    @staticmethod
    def calculate_distance(from_point: Tuple[float, float], to_point: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points."""
        dx = to_point[0] - from_point[0]
        dy = to_point[1] - from_point[1]
        return np.sqrt(dx**2 + dy**2)

    @staticmethod
    def plan_movements(path: List[Tuple[float, float]], start_position: Tuple[float, float] = (5.5, 5.5), start_angle: float = 0.0) -> List[Tuple[str, float]]:
        """
        Convert path to sequence of turtle movement commands.

        Returns:
            List of (command, value) tuples:
                ('move', distance) - move forward
                ('rotate', angle) - rotate in place
        """
        if len(path) < 2:
            return []

        movements = []
        current_pos = start_position
        current_angle = start_angle

        for next_pos in path:
            # Calculate movement needed
            distance = PathPlanner.calculate_distance(current_pos, next_pos)

            if distance > 0.01:  # Ignore very small movements
                # Calculate required rotation
                target_angle = PathPlanner.calculate_angle(current_pos, next_pos)
                angle_diff = target_angle - current_angle

                # Normalize angle difference to [-pi, pi]
                while angle_diff > np.pi:
                    angle_diff -= 2 * np.pi
                while angle_diff < -np.pi:
                    angle_diff += 2 * np.pi

                # Add rotation command if needed
                if abs(angle_diff) > 0.01:
                    movements.append(('rotate', float(np.degrees(angle_diff))))

                # Add movement command
                movements.append(('move', float(distance)))

                current_pos = next_pos
                current_angle = target_angle

        return movements

    @staticmethod
    def smooth_path(path: List[Tuple[float, float]], window_size: int = 3) -> List[Tuple[float, float]]:
        """
        Smooth path using moving average to reduce jitter.
        """
        if len(path) < window_size:
            return path

        smoothed = []
        half_window = window_size // 2

        for i in range(len(path)):
            start_idx = max(0, i - half_window)
            end_idx = min(len(path), i + half_window + 1)

            window = path[start_idx:end_idx]
            avg_x = np.mean([p[0] for p in window])
            avg_y = np.mean([p[1] for p in window])

            smoothed.append((avg_x, avg_y))

        return smoothed

    @staticmethod
    def decimate_path(path: List[Tuple[float, float]], max_points: int = 100) -> List[Tuple[float, float]]:
        """
        Reduce number of points in path while preserving shape.
        Useful for very long contours.
        """
        if len(path) <= max_points:
            return path

        step = len(path) // max_points
        return path[::step]

    @staticmethod
    def clip_to_bounds(point: Tuple[float, float], bounds: Tuple[float, float, float, float]) -> Tuple[float, float]:
        """Clip point to stay within bounds."""
        min_x, min_y, max_x, max_y = bounds
        x = np.clip(point[0], min_x, max_x)
        y = np.clip(point[1], min_y, max_y)
        return (x, y)
