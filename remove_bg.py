# ==========================================
# Upscale-BGRemover
# File    : remove_bg.py
# Version : v0.1.0
# ==========================================

import sys
import cv2
import numpy as np
from PIL import Image


def validate_arguments():
    if len(sys.argv) != 3:
        print("Usage: python remove_bg.py input.png output.png")
        sys.exit(1)

    return sys.argv[1], sys.argv[2]


def load_image(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if img is None:
        print("Image not found.")
        sys.exit(1)

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)

    elif img.shape[2] == 3:
        b, g, r = cv2.split(img)
        alpha = np.full(b.shape, 255, dtype=np.uint8)
        img = cv2.merge((b, g, r, alpha))

    return img


def detect_circle(img):
    gray = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)

    blur_size = max(5, (min(gray.shape[:2]) // 100) * 2 + 1)
    gray = cv2.GaussianBlur(gray, (blur_size, blur_size), 2)

    min_size = min(gray.shape[:2])

    radius_ratio = 0.48
    radius_tolerance = 0.025

    min_radius = max(
        int(min_size * (radius_ratio - radius_tolerance)),
        int(min_size * 0.44),
    )

    max_radius = min(
        int(min_size * (radius_ratio + radius_tolerance)),
        int(min_size * 0.495),
    )

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.0,
        minDist=min_size,
        param1=120,
        param2=28,
        minRadius=min_radius,
        maxRadius=max_radius,
    )

    if circles is None:
        print("Circle not found.")
        sys.exit(1)

    circles = np.round(circles[0]).astype(int)

    best_circle = max(
        circles,
        key=lambda c: (
            c[2],
            -((c[0] - gray.shape[1] // 2) ** 2 + (c[1] - gray.shape[0] // 2) ** 2),
        ),
    )

    return best_circle


def create_mask(img, x, y, r):
    mask = np.zeros(
        img.shape[:2],
        dtype=np.uint8,
    )

    cv2.circle(
        mask,
        (x, y),
        r - 3,
        255,
        -1,
    )

    return mask


def crop_to_circle(img, x, y, r):
    padding = max(
        10,
        int(r * 0.03),
    )

    left = max(
        x - r - padding,
        0,
    )

    top = max(
        y - r - padding,
        0,
    )

    right = min(
        x + r + padding,
        img.shape[1],
    )

    bottom = min(
        y + r + padding,
        img.shape[0],
    )

    return img[
        top:bottom,
        left:right,
    ]


def apply_mask(img, mask):
    img[:, :, 3] = mask

    return img


def save_image(img, output_path):
    Image.fromarray(
        cv2.cvtColor(
            img,
            cv2.COLOR_BGRA2RGBA,
        )
    ).save(output_path)


def normalize_to_square(img):
    h, w = img.shape[:2]

    size = max(
        h,
        w,
    )

    canvas = np.zeros(
        (size, size, 4),
        dtype=np.uint8,
    )

    x = (size - w) // 2
    y = (size - h) // 2

    canvas[
        y : y + h,
        x : x + w,
    ] = img

    return canvas


def save_debug_image(img, x, y, r):
    debug = img.copy()

    cv2.circle(
        debug,
        (x, y),
        r,
        (0, 0, 255, 255),
        6,
    )

    cv2.imwrite(
        "debug_circle.png",
        debug,
    )

    print("Debug image saved: debug_circle.png")


def main():
    input_path, output_path = validate_arguments()

    img = load_image(
        input_path,
    )

    img = normalize_to_square(
        img,
    )

    x, y, r = detect_circle(
        img,
    )

    img = crop_to_circle(
        img,
        x,
        y,
        r,
    )

    x, y, r = detect_circle(
        img,
    )

    mask = create_mask(
        img,
        x,
        y,
        r,
    )

    img = apply_mask(
        img,
        mask,
    )

    save_image(
        img,
        output_path,
    )

    save_debug_image(
        img,
        x,
        y,
        r,
    )

    print(
        "Saved:",
        output_path,
    )


if __name__ == "__main__":
    main()
