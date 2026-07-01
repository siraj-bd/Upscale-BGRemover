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

    if img.shape[2] == 3:
        b, g, r = cv2.split(img)
        alpha = np.full(b.shape, 255, dtype=np.uint8)
        img = cv2.merge((b, g, r, alpha))

    return img

input_path, output_path = validate_arguments()

def detect_circle(img):
    gray = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.1,
        minDist=gray.shape[0],
        param1=120,
        param2=30,
        minRadius=int(min(gray.shape[:2]) * 0.43),
        maxRadius=int(min(gray.shape[:2]) * 0.495),
    )

    if circles is None:
        print("Circle not found.")
        sys.exit(1)

    circles = np.round(circles[0]).astype(int)

    return max(circles, key=lambda c: c[2])


img = load_image(input_path)

def create_mask(shape, x, y, r):
    mask = np.zeros(shape, dtype=np.uint8)

    cv2.circle(
        mask,
        (x, y),
        r - 3,
        255,
        -1,
    )

    return mask


x, y, r = detect_circle(img)

gray = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)

def apply_mask(img, mask):
    img[:, :, 3] = mask

    return img

mask = create_mask(gray.shape, x, y, r)

def save_image(img, output_path):
    Image.fromarray(
        cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    ).save(output_path)

img = apply_mask(img, mask)

save_image(img, output_path)

debug = img.copy()
cv2.circle(debug, (x, y), r, (0, 0, 255, 255), 6)
cv2.imwrite("debug_circle.png", debug)
print("Debug image saved: debug_circle.png")

print("Saved:", output_path)