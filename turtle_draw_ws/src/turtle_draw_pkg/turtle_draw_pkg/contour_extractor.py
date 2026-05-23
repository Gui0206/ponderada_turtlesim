import numpy as np
from typing import List, Tuple


class ContourExtractor:
    """
    Extract contours from binary images using connected component analysis.
    Implements contour tracing algorithms from scratch.
    """

    @staticmethod
    def find_contours(binary_image: np.ndarray) -> List[np.ndarray]:
        """
        Find all contours in binary image using Moore-Neighbor tracing algorithm.
        Returns list of contours, where each contour is an array of (x, y) coordinates.
        """
        contours = []
        visited = np.zeros_like(binary_image, dtype=bool)

        h, w = binary_image.shape

        for i in range(h):
            for j in range(w):
                if binary_image[i, j] > 0 and not visited[i, j]:
                    contour = ContourExtractor._trace_contour(binary_image, i, j, visited)
                    if len(contour) > 5:  # Filter out very small contours
                        contours.append(contour)

        return contours

    @staticmethod
    def _trace_contour(binary_image: np.ndarray, start_i: int, start_j: int, visited: np.ndarray) -> np.ndarray:
        """
        Trace a single contour using Moore-Neighbor algorithm.
        Returns array of (x, y) coordinates forming the contour.
        """
        h, w = binary_image.shape
        contour = []

        # Direction vectors: right, down-right, down, down-left, left, up-left, up, up-right
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        current_i, current_j = start_i, start_j
        direction_idx = 0

        while True:
            visited[current_i, current_j] = True
            contour.append([current_j, current_i])  # Store as (x, y)

            # Try to find next point in contour
            found_next = False
            for attempt in range(8):
                next_direction = (direction_idx + attempt) % 8
                di, dj = directions[next_direction]
                next_i, next_j = current_i + di, current_j + dj

                if 0 <= next_i < h and 0 <= next_j < w and binary_image[next_i, next_j] > 0:
                    if not visited[next_i, next_j] or (next_i == start_i and next_j == start_j):
                        current_i, current_j = next_i, next_j
                        direction_idx = next_direction
                        found_next = True
                        break

            if not found_next or (current_i == start_i and current_j == start_j):
                break

        return np.array(contour, dtype=np.float32)

    @staticmethod
    def filter_contours_by_size(contours: List[np.ndarray], min_size: int = 5, max_size: int = None) -> List[np.ndarray]:
        """Filter contours by number of points."""
        filtered = []
        for contour in contours:
            if len(contour) >= min_size:
                if max_size is None or len(contour) <= max_size:
                    filtered.append(contour)
        return filtered

    @staticmethod
    def simplify_contour(contour: np.ndarray, epsilon: float = 2.0) -> np.ndarray:
        """
        Simplify contour using Ramer-Douglas-Peucker algorithm.
        Reduces number of points while preserving shape.
        """
        if len(contour) < 3:
            return contour

        dmax = 0
        index = 0

        end = len(contour) - 1
        for i in range(1, end):
            d = ContourExtractor._point_to_line_distance(
                contour[i],
                contour[0],
                contour[end]
            )
            if d > dmax:
                dmax = d
                index = i

        if dmax > epsilon:
            rec1 = ContourExtractor.simplify_contour(contour[:index + 1], epsilon)
            rec2 = ContourExtractor.simplify_contour(contour[index:], epsilon)
            return np.concatenate((rec1[:-1], rec2))
        else:
            return np.array([contour[0], contour[end]])

    @staticmethod
    def _point_to_line_distance(point: np.ndarray, line_start: np.ndarray, line_end: np.ndarray) -> float:
        """Calculate perpendicular distance from point to line."""
        px, py = point
        x1, y1 = line_start
        x2, y2 = line_end

        numerator = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1)
        denominator = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

        if denominator == 0:
            return np.sqrt((px - x1) ** 2 + (py - y1) ** 2)

        return numerator / denominator

    @staticmethod
    def order_contour_points(contour: np.ndarray) -> np.ndarray:
        """
        Order contour points to ensure smooth drawing.
        Uses nearest-neighbor approach starting from top-left.
        """
        if len(contour) == 0:
            return contour

        # Start from top-left point
        start_idx = np.argmin(contour[:, 1] + contour[:, 0])
        ordered = [contour[start_idx]]
        remaining = set(range(len(contour))) - {start_idx}

        while remaining:
            current = ordered[-1]
            distances = [np.linalg.norm(contour[i] - current) for i in remaining]
            next_idx = list(remaining)[np.argmin(distances)]
            ordered.append(contour[next_idx])
            remaining.remove(next_idx)

        return np.array(ordered)

    @staticmethod
    def merge_nearby_contours(contours: List[np.ndarray], distance_threshold: float = 50) -> List[np.ndarray]:
        """
        Merge contours that are very close to each other.
        Helps reduce fragmentation.
        """
        if len(contours) == 0:
            return contours

        merged = []
        used = set()

        for i, contour1 in enumerate(contours):
            if i in used:
                continue

            current_contour = contour1.copy()

            for j, contour2 in enumerate(contours):
                if i != j and j not in used:
                    # Check if contours are close
                    min_distance = min(
                        np.min(np.linalg.norm(contour1[:, np.newaxis] - contour2, axis=2)),
                        np.min(np.linalg.norm(contour2[:, np.newaxis] - contour1, axis=2))
                    )

                    if min_distance < distance_threshold:
                        current_contour = np.concatenate([current_contour, contour2])
                        used.add(j)

            merged.append(current_contour)
            used.add(i)

        return merged
