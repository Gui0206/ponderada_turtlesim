"""
Computer vision pipeline for extracting image contours.
All image processing implemented from scratch using only NumPy.
"""

import cv2
import numpy as np
from typing import Tuple, List


class ImageProcessor:
    """Handles all image preprocessing and edge detection."""

    def __init__(self):
        self.original = None
        self.grayscale = None
        self.preprocessed = None
        self.edges = None
        self.contours = None

    def load_image(self, image_path: str) -> np.ndarray:
        """Load image using OpenCV (allowed by requirements)."""
        self.original = cv2.imread(image_path)
        if self.original is None:
            raise ValueError(f"Could not load image from {image_path}")
        return self.original

    def to_grayscale(self, image: np.ndarray = None) -> np.ndarray:
        """Convert BGR to grayscale using standard luminosity formula."""
        if image is None:
            image = self.original

        # Standard RGB to grayscale: 0.299*R + 0.587*G + 0.114*B
        # OpenCV uses BGR, so: 0.299*B + 0.587*G + 0.114*R
        b, g, r = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        self.grayscale = (0.114 * r + 0.587 * g + 0.299 * b).astype(np.uint8)
        return self.grayscale

    def gaussian_blur(self, image: np.ndarray = None, kernel_size: int = 5, sigma: float = 1.0) -> np.ndarray:
        """Apply Gaussian blur using separable convolution (from scratch)."""
        if image is None:
            image = self.grayscale

        # Create 1D Gaussian kernel
        kernel_1d = self._gaussian_kernel_1d(kernel_size, sigma)

        # Apply horizontal convolution
        blurred_h = self._convolve_1d(image, kernel_1d, axis=1)

        # Apply vertical convolution
        blurred = self._convolve_1d(blurred_h, kernel_1d, axis=0)

        return blurred.astype(np.uint8)

    def _gaussian_kernel_1d(self, size: int, sigma: float) -> np.ndarray:
        """Create 1D Gaussian kernel."""
        kernel = np.zeros(size)
        center = size // 2
        for x in range(size):
            kernel[x] = np.exp(-((x - center) ** 2) / (2 * sigma ** 2))
        kernel /= np.sum(kernel)
        return kernel

    def _convolve_1d(self, image: np.ndarray, kernel: np.ndarray, axis: int) -> np.ndarray:
        """Apply 1D convolution along specified axis."""
        kernel_size = len(kernel)
        pad = kernel_size // 2

        if axis == 0:  # Vertical
            padded = np.pad(image, ((pad, pad), (0, 0)), mode='edge')
            result = np.zeros_like(image, dtype=np.float32)
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    result[i, j] = np.sum(kernel * padded[i:i+kernel_size, j])
        else:  # Horizontal
            padded = np.pad(image, ((0, 0), (pad, pad)), mode='edge')
            result = np.zeros_like(image, dtype=np.float32)
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    result[i, j] = np.sum(kernel * padded[i, j:j+kernel_size])

        return result

    def threshold(self, image: np.ndarray = None, threshold_val: int = 127) -> np.ndarray:
        """Binary thresholding."""
        if image is None:
            image = self.preprocessed if self.preprocessed is not None else self.grayscale

        return (image > threshold_val).astype(np.uint8) * 255

    def sobel_edge_detection(self, image: np.ndarray = None) -> np.ndarray:
        """Detect edges using Sobel operator (implemented from scratch)."""
        if image is None:
            image = self.grayscale

        # Sobel kernels
        sobel_x = np.array([[-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1]], dtype=np.float32)

        sobel_y = np.array([[-1, -2, -1],
                            [0, 0, 0],
                            [1, 2, 1]], dtype=np.float32)

        # Apply convolution
        gx = self._convolve_2d(image, sobel_x)
        gy = self._convolve_2d(image, sobel_y)

        # Magnitude
        magnitude = np.sqrt(gx**2 + gy**2)
        magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8)

        self.edges = magnitude
        return magnitude

    def _convolve_2d(self, image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """Apply 2D convolution."""
        kernel_h, kernel_w = kernel.shape
        pad_h, pad_w = kernel_h // 2, kernel_w // 2

        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
        result = np.zeros_like(image, dtype=np.float32)

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                region = padded[i:i+kernel_h, j:j+kernel_w]
                result[i, j] = np.sum(region * kernel)

        return result

    def preprocess(self, image: np.ndarray = None) -> np.ndarray:
        """Complete preprocessing pipeline."""
        if image is None:
            image = self.grayscale

        # Apply Gaussian blur to reduce noise
        blurred = self.gaussian_blur(image, kernel_size=5, sigma=1.5)

        # Apply Sobel edge detection
        edges = self.sobel_edge_detection(blurred)

        # Threshold edges
        self.preprocessed = self.threshold(edges, threshold_val=50)

        return self.preprocessed

    def extract_contours(self, edges: np.ndarray = None, min_length: int = 10) -> List[np.ndarray]:
        """Extract contours using simple connected component labeling."""
        if edges is None:
            edges = self.preprocessed if self.preprocessed is not None else self.edges

        # Make a copy to avoid modifying original
        labeled = edges.copy()
        contours_list = []

        # Find all white pixels and trace contours
        h, w = labeled.shape
        visited = np.zeros_like(labeled, dtype=bool)

        for y in range(h):
            for x in range(w):
                if labeled[y, x] > 0 and not visited[y, x]:
                    # Trace this contour
                    contour = self._trace_contour(labeled, visited, x, y)
                    if len(contour) > min_length:
                        contours_list.append(contour)

        self.contours = contours_list
        return contours_list

    def _trace_contour(self, edges: np.ndarray, visited: np.ndarray, start_x: int, start_y: int) -> np.ndarray:
        """Trace a single contour using flood fill."""
        h, w = edges.shape
        stack = [(start_x, start_y)]
        contour_points = []

        while stack:
            x, y = stack.pop()

            if x < 0 or x >= w or y < 0 or y >= h:
                continue
            if visited[y, x] or edges[y, x] == 0:
                continue

            visited[y, x] = True
            contour_points.append([x, y])

            # 8-connectivity: check all 8 neighbors
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx] and edges[ny, nx] > 0:
                        stack.append((nx, ny))

        return np.array(contour_points, dtype=np.int32)

    def get_contour_skeleton(self, contour: np.ndarray, max_points: int = 100) -> np.ndarray:
        """Downsample contour to manageable number of points."""
        if len(contour) <= max_points:
            return contour

        # Simple uniform sampling
        step = len(contour) // max_points
        if step < 1:
            step = 1
        return contour[::step]


class CoordinateMapper:
    """Maps image coordinates to turtle coordinate space."""

    def __init__(self, image_shape: Tuple[int, int], turtle_bounds: Tuple[float, float, float, float]):
        """
        Initialize mapper.
        turtle_bounds: (min_x, max_x, min_y, max_y) in turtle coordinate space
        """
        self.image_height, self.image_width = image_shape[:2]
        self.turtle_min_x, self.turtle_max_x, self.turtle_min_y, self.turtle_max_y = turtle_bounds

    def map_point(self, img_x: float, img_y: float) -> Tuple[float, float]:
        """Map image coordinates to turtle coordinates."""
        # Normalize to [0, 1]
        norm_x = img_x / self.image_width
        norm_y = img_y / self.image_height

        # Map to turtle bounds
        turtle_x = self.turtle_min_x + norm_x * (self.turtle_max_x - self.turtle_min_x)
        turtle_y = self.turtle_max_y - norm_y * (self.turtle_max_y - self.turtle_min_y)  # Flip Y

        return turtle_x, turtle_y

    def map_contour(self, contour: np.ndarray) -> np.ndarray:
        """Map all points in a contour."""
        mapped = np.zeros_like(contour, dtype=np.float32)
        for i, point in enumerate(contour):
            mapped[i] = self.map_point(point[0], point[1])
        return mapped
