#!/usr/bin/env python3
"""
Standalone test script for vision pipeline.
Tests image processing without requiring ROS.
"""

import sys
import os

# Add workspace to path
sys.path.insert(0, '/Users/guilhermeholanda/Desktop/ponderada_ros/turtle_draw_ws/src/turtle_draw_pkg')

import numpy as np
import matplotlib.pyplot as plt

try:
    from turtle_draw_pkg.vision_pipeline import ImageProcessor, CoordinateMapper
    print("✅ Successfully imported vision_pipeline module")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)

def test_vision_pipeline():
    """Test the complete vision pipeline."""

    image_path = '/Users/guilhermeholanda/Desktop/ponderada_ros/dog.png'

    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return False

    print(f"\n📷 Loading image: {image_path}")
    processor = ImageProcessor()

    try:
        # Load image
        image = processor.load_image(image_path)
        print(f"✅ Image loaded: shape={image.shape}")

        # Convert to grayscale
        grayscale = processor.to_grayscale()
        print(f"✅ Grayscale conversion: shape={grayscale.shape}, dtype={grayscale.dtype}")

        # Gaussian blur
        blurred = processor.gaussian_blur(grayscale, kernel_size=5, sigma=1.5)
        print(f"✅ Gaussian blur: shape={blurred.shape}")

        # Sobel edge detection
        edges = processor.sobel_edge_detection(blurred)
        print(f"✅ Sobel edge detection: shape={edges.shape}, min={edges.min()}, max={edges.max()}")

        # Threshold
        threshold = processor.threshold(edges, threshold_val=50)
        print(f"✅ Thresholding: {np.sum(threshold > 0)} edge pixels")

        # Contour extraction
        contours = processor.extract_contours(threshold, min_length=5)
        print(f"✅ Contour extraction: {len(contours)} contours found")

        if contours:
            for i, contour in enumerate(contours[:3]):
                print(f"   - Contour {i+1}: {len(contour)} points")

        # Coordinate mapping
        mapper = CoordinateMapper(image.shape, (0.5, 10.5, 0.5, 10.5))
        print(f"✅ Coordinate mapper initialized")

        if contours:
            mapped = mapper.map_contour(contours[0])
            print(f"✅ Mapping: {contours[0].shape} -> {mapped.shape}")
            print(f"   Range: x=[{mapped[:,0].min():.2f}, {mapped[:,0].max():.2f}], "
                  f"y=[{mapped[:,1].min():.2f}, {mapped[:,1].max():.2f}]")

        # Create visualization
        print("\n📊 Creating visualization...")
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))

        # Original
        import cv2
        axes[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('Original Image')
        axes[0, 0].axis('off')

        # Grayscale
        axes[0, 1].imshow(grayscale, cmap='gray')
        axes[0, 1].set_title('Grayscale')
        axes[0, 1].axis('off')

        # Blurred
        axes[0, 2].imshow(blurred, cmap='gray')
        axes[0, 2].set_title('Gaussian Blur')
        axes[0, 2].axis('off')

        # Edges
        axes[1, 0].imshow(edges, cmap='gray')
        axes[1, 0].set_title('Sobel Edges')
        axes[1, 0].axis('off')

        # Thresholded
        axes[1, 1].imshow(threshold, cmap='gray')
        axes[1, 1].set_title('Thresholded Edges')
        axes[1, 1].axis('off')

        # Contours overlay
        contour_image = np.zeros_like(threshold)
        for contour in contours:
            for point in contour:
                x, y = point
                if 0 <= x < contour_image.shape[1] and 0 <= y < contour_image.shape[0]:
                    contour_image[y, x] = 255

        axes[1, 2].imshow(contour_image, cmap='gray')
        axes[1, 2].set_title(f'Contours ({len(contours)})')
        axes[1, 2].axis('off')

        plt.tight_layout()
        output_path = '/Users/guilhermeholanda/Desktop/ponderada_ros/vision_pipeline_visualization.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ Visualization saved: {output_path}")

        # Print summary
        print("\n" + "="*50)
        print("✅ VISION PIPELINE TEST PASSED")
        print("="*50)
        print(f"Contours detected: {len(contours)}")
        print(f"Image size: {image.shape[0]}x{image.shape[1]}")
        print(f"Edge pixels: {np.sum(threshold > 0)}")
        print("="*50)

        return True

    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n" + "="*50)
    print("TURTLE DRAW - Vision Pipeline Test")
    print("="*50)

    success = test_vision_pipeline()
    sys.exit(0 if success else 1)
