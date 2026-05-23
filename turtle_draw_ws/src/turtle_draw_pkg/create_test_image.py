#!/usr/bin/env python3
"""Create test images for turtle_draw."""

import numpy as np
import cv2


def create_simple_shapes():
    """Create image with simple geometric shapes."""
    img = np.ones((400, 400), dtype=np.uint8) * 255  # White background

    # Draw black shapes
    # Square
    cv2.rectangle(img, (50, 50), (150, 150), 0, 2)

    # Circle
    cv2.circle(img, (300, 100), 40, 0, 2)

    # Triangle
    pts = np.array([[250, 250], [350, 250], [300, 320]], dtype=np.int32)
    cv2.polylines(img, [pts], True, 0, 2)

    # Line
    cv2.line(img, (50, 250), (200, 350), 0, 2)

    cv2.imwrite('test_shapes.png', img)
    print('Created test_shapes.png')


def create_letter():
    """Create image with a letter."""
    img = np.ones((300, 200), dtype=np.uint8) * 255

    # Draw letter 'A'
    cv2.putText(img, 'A', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, 0, 3)

    cv2.imwrite('test_letter.png', img)
    print('Created test_letter.png')


def create_spiral():
    """Create image with a spiral."""
    img = np.ones((400, 400), dtype=np.uint8) * 255

    center = (200, 200)
    for i in range(100):
        angle = i * 0.1
        radius = i * 1.5
        x = int(center[0] + radius * np.cos(angle))
        y = int(center[1] + radius * np.sin(angle))

        if i > 0:
            cv2.line(img, last_point, (x, y), 0, 2)
        last_point = (x, y)

    cv2.imwrite('test_spiral.png', img)
    print('Created test_spiral.png')


def create_grid():
    """Create image with grid pattern."""
    img = np.ones((300, 300), dtype=np.uint8) * 255

    for i in range(0, 300, 50):
        cv2.line(img, (i, 0), (i, 300), 0, 1)
        cv2.line(img, (0, i), (300, i), 0, 1)

    cv2.imwrite('test_grid.png', img)
    print('Created test_grid.png')


if __name__ == '__main__':
    create_simple_shapes()
    create_letter()
    create_spiral()
    create_grid()
    print('All test images created!')
