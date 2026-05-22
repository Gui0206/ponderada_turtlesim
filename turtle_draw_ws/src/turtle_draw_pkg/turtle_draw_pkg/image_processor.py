"""
Standalone image processor node for testing and visualization.
"""

import rclpy
from rclpy.node import Node
import matplotlib.pyplot as plt
import numpy as np
import sys
from turtle_draw_pkg.vision_pipeline import ImageProcessor, CoordinateMapper


class ImageProcessorNode(Node):
    """Node for processing and visualizing image contours."""

    def __init__(self):
        super().__init__('image_processor')
        self.get_logger().info("Image Processor Node initialized")

    def process_and_visualize(self, image_path: str):
        """Process image and show visualization."""
        self.get_logger().info(f"Processing: {image_path}")

        processor = ImageProcessor()

        # Load and convert to grayscale
        image = processor.load_image(image_path)
        grayscale = processor.to_grayscale()

        # Preprocess
        preprocessed = processor.preprocess()

        # Extract contours
        contours = processor.extract_contours(min_length=5)
        self.get_logger().info(f"Found {len(contours)} contours")

        # Visualization
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Vision Pipeline: Image Processing Steps', fontsize=16)

        # Original
        axes[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('Original Image')
        axes[0, 0].axis('off')

        # Grayscale
        axes[0, 1].imshow(grayscale, cmap='gray')
        axes[0, 1].set_title('Grayscale')
        axes[0, 1].axis('off')

        # Blurred (during preprocessing)
        blurred = processor.gaussian_blur(grayscale)
        axes[0, 2].imshow(blurred, cmap='gray')
        axes[0, 2].set_title('Gaussian Blur')
        axes[0, 2].axis('off')

        # Edges
        axes[1, 0].imshow(processor.edges, cmap='gray')
        axes[1, 0].set_title('Sobel Edge Detection')
        axes[1, 0].axis('off')

        # Thresholded edges
        axes[1, 1].imshow(preprocessed, cmap='gray')
        axes[1, 1].set_title('Thresholded Edges')
        axes[1, 1].axis('off')

        # Contours overlay
        contour_image = np.zeros_like(preprocessed)
        for contour in contours:
            for point in contour:
                x, y = point
                if 0 <= x < contour_image.shape[1] and 0 <= y < contour_image.shape[0]:
                    contour_image[y, x] = 255

        axes[1, 2].imshow(contour_image, cmap='gray')
        axes[1, 2].set_title(f'Extracted Contours ({len(contours)})')
        axes[1, 2].axis('off')

        plt.tight_layout()
        plt.savefig('/Users/guilhermeholanda/Desktop/ponderada_ros/vision_pipeline_visualization.png', dpi=150)
        self.get_logger().info("Visualization saved to vision_pipeline_visualization.png")
        plt.show()

        # Print contour statistics
        self.get_logger().info("\n=== Contour Statistics ===")
        for i, contour in enumerate(contours[:5]):  # Show first 5
            self.get_logger().info(f"Contour {i+1}: {len(contour)} points")


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)

    # Import here to avoid circular dependencies
    import cv2

    node = ImageProcessorNode()

    image_path = '/Users/guilhermeholanda/Desktop/ponderada_ros/dog.png'
    if len(sys.argv) > 1:
        image_path = sys.argv[1]

    try:
        node.process_and_visualize(image_path)
    except Exception as e:
        node.get_logger().error(f"Error: {str(e)}")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
