import sys
import cv2
import numpy as np
from PIL import Image

if len(sys.argv) != 3:
    print("Usage: python3 remove_bg.py input.png output.png")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

if img is None:
    print("Image not found.")
    sys.exit(1)

if img.shape[2] == 3:
    b, g, r = cv2.split(img)
    alpha = np.full(b.shape, 255, dtype=np.uint8)
    img = cv2.merge((b, g, r, alpha))

gray = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (9, 9), 2)

circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=gray.shape[0] // 2,
    param1=100,
    param2=40,
    minRadius=int(min(gray.shape[:2]) * 0.35),
    maxRadius=int(min(gray.shape[:2]) * 0.49),
)

if circles is None:
    print("Circle not found.")
    sys.exit(1)

circles = np.round(circles[0]).astype(int)

largest = max(circles, key=lambda c: c[2])

x, y, r = largest

mask = np.zeros(gray.shape, dtype=np.uint8)

cv2.circle(mask, (x, y), r - 2, 255, -1)

img[:, :, 3] = mask

Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)).save(output_path)

print("Saved:", output_path)