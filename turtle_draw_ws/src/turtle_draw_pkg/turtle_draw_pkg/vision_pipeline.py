#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys

from .image_processor import ImageProcessor
from .contour_extractor import ContourExtractor
from .path_planner import PathPlanner


def visualize_pipeline(image_path: str, output_dir: str = None):
    """
    Visualize each step of the computer vision pipeline.
    Saves images showing preprocessing, edge detection, contours, etc.
    """
    print(f'Loading image from: {image_path}')

    # Load image
    image = ImageProcessor.load_image(image_path)
    print(f'Original image shape: {image.shape}')

    # Normalize
    normalized = image.astype(np.float32) / 255.0

    # Gaussian blur
    print('Applying Gaussian blur...')
    blurred = ImageProcessor.gaussian_blur(normalized, kernel_size=5, sigma=1.5)

    # Sobel edge detection
    print('Detecting edges with Sobel...')
    magnitude, direction = ImageProcessor.sobel_edge_detection(blurred)
    magnitude_normalized = magnitude / (np.max(magnitude) + 1e-8)

    # Non-maximum suppression
    print('Applying non-maximum suppression...')
    suppressed = ImageProcessor.non_maximum_suppression(magnitude, direction)
    suppressed_normalized = suppressed / (np.max(suppressed) + 1e-8)

    # Thresholding
    print('Thresholding...')
    threshold = 0.1
    binary = ImageProcessor.threshold(suppressed_normalized, threshold_value=threshold)

    # Extract contours
    print('Extracting contours...')
    contours = ContourExtractor.find_contours(binary)
    print(f'Found {len(contours)} contours')

    # Filter contours
    filtered_contours = ContourExtractor.filter_contours_by_size(contours, min_size=10)
    print(f'After filtering: {len(filtered_contours)} contours')

    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Computer Vision Pipeline - Turtle Draw', fontsize=16)

    # Original image
    axes[0, 0].imshow(image, cmap='gray')
    axes[0, 0].set_title('Original Image')
    axes[0, 0].axis('off')

    # Blurred
    axes[0, 1].imshow(blurred, cmap='gray')
    axes[0, 1].set_title('Gaussian Blur (σ=1.5)')
    axes[0, 1].axis('off')

    # Sobel magnitude
    axes[0, 2].imshow(magnitude_normalized, cmap='hot')
    axes[0, 2].set_title('Sobel Edge Magnitude')
    axes[0, 2].axis('off')

    # Non-maximum suppression
    axes[1, 0].imshow(suppressed_normalized, cmap='hot')
    axes[1, 0].set_title('Non-Maximum Suppression')
    axes[1, 0].axis('off')

    # Binary image
    axes[1, 1].imshow(binary, cmap='gray')
    axes[1, 1].set_title(f'Binary Image (threshold={threshold})')
    axes[1, 1].axis('off')

    # Contours visualization
    contour_img = np.zeros_like(binary)
    for contour in filtered_contours:
        for point in contour:
            x, y = int(point[0]), int(point[1])
            if 0 <= y < contour_img.shape[0] and 0 <= x < contour_img.shape[1]:
                contour_img[y, x] = 255

    axes[1, 2].imshow(contour_img, cmap='gray')
    axes[1, 2].set_title(f'Extracted Contours ({len(filtered_contours)} found)')
    axes[1, 2].axis('off')

    plt.tight_layout()

    if output_dir:
        output_path = f'{output_dir}/pipeline_visualization.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f'Saved visualization to: {output_path}')
    else:
        plt.savefig('pipeline_visualization.png', dpi=150, bbox_inches='tight')
        print('Saved visualization to: pipeline_visualization.png')

    plt.show()

    # Print statistics
    print('\n=== Pipeline Statistics ===')
    print(f'Original image size: {image.shape}')
    print(f'Number of contours found: {len(contours)}')
    print(f'Number of contours after filtering: {len(filtered_contours)}')

    if filtered_contours:
        sizes = [len(c) for c in filtered_contours]
        print(f'Contour sizes - Min: {min(sizes)}, Max: {max(sizes)}, Mean: {np.mean(sizes):.1f}')

    # Visualize paths in turtle space
    print('\n=== Planning paths in turtle space ===')
    planner = PathPlanner(image.shape)
    paths = planner.contours_to_paths(filtered_contours)
    print(f'Number of paths: {len(paths)}')

    if paths:
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, 11)
        ax.set_ylim(0, 11)
        ax.set_aspect('equal')
        ax.set_title('Turtle Drawing Space')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True, alpha=0.3)

        colors = plt.cm.rainbow(np.linspace(0, 1, len(paths)))

        for path_idx, path in enumerate(paths):
            xs = [p[0] for p in path]
            ys = [p[1] for p in path]
            ax.plot(xs, ys, color=colors[path_idx], alpha=0.7, linewidth=2, label=f'Path {path_idx + 1}')

        ax.scatter([5.5], [5.5], color='red', s=100, marker='o', label='Start position', zorder=5)
        ax.legend()

        plt.tight_layout()
        plt.savefig('turtle_paths.png', dpi=150, bbox_inches='tight')
        print('Saved path visualization to: turtle_paths.png')
        plt.show()


def main(args=None):
    parser = argparse.ArgumentParser(description='Visualize computer vision pipeline')
    parser.add_argument('image', nargs='?', help='Path to image file')
    parser.add_argument('-o', '--output', help='Output directory for images')
    args = parser.parse_args(args)

    if args.image is None:
        print('Usage: vision_pipeline <image_path> [-o output_dir]')
        return

    visualize_pipeline(args.image, args.output)


if __name__ == '__main__':
    main()
