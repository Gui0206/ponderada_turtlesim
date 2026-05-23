import numpy as np
import cv2
from typing import Tuple


class ImageProcessor:
    """
    Computer vision pipeline for edge detection and preprocessing.
    Implements all algorithms from scratch using NumPy only.
    """

    def __init__(self):
        pass

    @staticmethod
    def load_image(image_path: str) -> np.ndarray:
        """Load image using OpenCV (only allowed use of OpenCV)."""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Could not load image from {image_path}")
        return img

    @staticmethod
    def gaussian_blur(image: np.ndarray, kernel_size: int = 5, sigma: float = 1.0) -> np.ndarray:
        """
        Apply Gaussian blur using separable convolution (from scratch).
        Kernel size must be odd.
        """
        if kernel_size % 2 == 0:
            kernel_size += 1

        # Create 1D Gaussian kernel
        kernel = ImageProcessor._create_gaussian_kernel(kernel_size, sigma)

        # Normalize kernel
        kernel = kernel / np.sum(kernel)

        # Apply separable convolution (apply 1D twice - horizontal then vertical)
        blurred = ImageProcessor._convolve_1d(image, kernel, axis=1)
        blurred = ImageProcessor._convolve_1d(blurred, kernel, axis=0)

        return blurred

    @staticmethod
    def _create_gaussian_kernel(size: int, sigma: float) -> np.ndarray:
        """Create 1D Gaussian kernel."""
        kernel = np.arange(size) - (size - 1) / 2.0
        kernel = np.exp(-0.5 * (kernel / sigma) ** 2)
        return kernel

    @staticmethod
    def _convolve_1d(image: np.ndarray, kernel: np.ndarray, axis: int = 0) -> np.ndarray:
        """Apply 1D convolution along specified axis with padding."""
        kernel_size = len(kernel)
        pad_size = kernel_size // 2

        if axis == 0:
            padded = np.pad(image, ((pad_size, pad_size), (0, 0)), mode='reflect')
            output = np.zeros_like(image, dtype=np.float64)

            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    output[i, j] = np.sum(kernel * padded[i:i+kernel_size, j])
        else:
            padded = np.pad(image, ((0, 0), (pad_size, pad_size)), mode='reflect')
            output = np.zeros_like(image, dtype=np.float64)

            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    output[i, j] = np.sum(kernel * padded[i, j:j+kernel_size])

        return output.astype(image.dtype)

    @staticmethod
    def sobel_edge_detection(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Sobel edge detection from scratch.
        Returns magnitude and direction of edges.
        """
        # Sobel kernels
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)

        # Apply convolution
        gx = ImageProcessor._convolve_2d(image, sobel_x)
        gy = ImageProcessor._convolve_2d(image, sobel_y)

        # Calculate magnitude and direction
        magnitude = np.sqrt(gx**2 + gy**2)
        direction = np.arctan2(gy, gx)

        return magnitude, direction

    @staticmethod
    def _convolve_2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """Apply 2D convolution with reflection padding."""
        kernel_h, kernel_w = kernel.shape
        pad_h = kernel_h // 2
        pad_w = kernel_w // 2

        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
        output = np.zeros_like(image, dtype=np.float64)

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                region = padded[i:i+kernel_h, j:j+kernel_w]
                output[i, j] = np.sum(region * kernel)

        return output

    @staticmethod
    def non_maximum_suppression(magnitude: np.ndarray, direction: np.ndarray) -> np.ndarray:
        """
        Non-maximum suppression for Canny-like edge thinning.
        Suppresses pixels that are not local maxima in gradient direction.
        """
        h, w = magnitude.shape
        suppressed = np.zeros_like(magnitude)

        # Convert direction to degrees
        direction = np.degrees(direction) + 180
        direction[direction < 0] += 180

        for i in range(1, h - 1):
            for j in range(1, w - 1):
                angle = direction[i, j]
                current_magnitude = magnitude[i, j]

                # Determine neighbors based on edge direction
                if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                    # Horizontal
                    neighbor1 = magnitude[i, j + 1]
                    neighbor2 = magnitude[i, j - 1]
                elif 22.5 <= angle < 67.5:
                    # Diagonal \
                    neighbor1 = magnitude[i + 1, j - 1]
                    neighbor2 = magnitude[i - 1, j + 1]
                elif 67.5 <= angle < 112.5:
                    # Vertical
                    neighbor1 = magnitude[i + 1, j]
                    neighbor2 = magnitude[i - 1, j]
                else:
                    # Diagonal /
                    neighbor1 = magnitude[i + 1, j + 1]
                    neighbor2 = magnitude[i - 1, j - 1]

                if current_magnitude >= neighbor1 and current_magnitude >= neighbor2:
                    suppressed[i, j] = current_magnitude

        return suppressed

    @staticmethod
    def threshold(image: np.ndarray, threshold_value: float) -> np.ndarray:
        """Simple binary thresholding."""
        return (image > threshold_value).astype(np.uint8) * 255

    @staticmethod
    def preprocess(image: np.ndarray) -> np.ndarray:
        """
        Preprocess image: normalize, blur, and edge detect.
        """
        # Normalize to 0-1 range
        normalized = image.astype(np.float32) / 255.0

        # Apply Gaussian blur to reduce noise
        blurred = ImageProcessor.gaussian_blur(normalized, kernel_size=5, sigma=1.5)

        # Sobel edge detection
        magnitude, direction = ImageProcessor.sobel_edge_detection(blurred)

        # Non-maximum suppression
        suppressed = ImageProcessor.non_maximum_suppression(magnitude, direction)

        # Threshold to binary
        normalized_mag = suppressed / (np.max(suppressed) + 1e-8)
        binary = ImageProcessor.threshold(normalized_mag, threshold_value=0.1)

        return binary

    @staticmethod
    def dilate(image: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
        """
        Morphological dilation (from scratch).
        Expands white regions.
        """
        kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)

        for _ in range(iterations):
            padded = np.pad(image, kernel_size // 2, mode='constant', constant_values=0)
            dilated = np.zeros_like(image)

            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    region = padded[i:i+kernel_size, j:j+kernel_size]
                    dilated[i, j] = np.max(region * kernel)

            image = dilated

        return image

    @staticmethod
    def erode(image: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
        """
        Morphological erosion (from scratch).
        Shrinks white regions.
        """
        kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)

        for _ in range(iterations):
            padded = np.pad(image, kernel_size // 2, mode='constant', constant_values=255)
            eroded = np.zeros_like(image)

            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    region = padded[i:i+kernel_size, j:j+kernel_size]
                    eroded[i, j] = np.min(region)

            image = eroded

        return image
