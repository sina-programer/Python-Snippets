import numpy as np
import cv2

def opacity(color, alpha):
    if alpha > 1:
        alpha /= 100
    if len(color) == 4:
        color[-1] = alpha * 100
    else:
        color = list(map(lambda x: x*alpha, color))
    return tuple(map(int, color))

def circle(image, center, radius, color=None, feather=20, fill=True, thickness=20):
    if color is None:
        color = (0, 0, 0)
    t = -1 if fill else thickness
    r = 255 / feather
    color = list(color) + [255]
    for idx, i in enumerate(range(feather, 0, -1), start=1):
        cv2.circle(image, center, radius+i, opacity(color, idx*r), t)

def full_color():
    image = np.zeros(SHAPE)
    matrix = np.full((ROWS, COLS), -1)
    nr = np.random.choice([0, 1, 2, 3, 4], p=[.15, .15, .25, .35, .1], replace=False)  # number of removed circles
    colors = np.take(COLORS, np.random.permutation(len(COLORS))[:-nr], axis=0)

    for ci, color in enumerate(colors):
        for i in range(ROWS):
            j = np.random.choice(np.where(matrix[i] == -1)[0])
            matrix[i, j] = ci
            center = (
                (j+1) * CL - CL//2,
                (i+1)  *RL - RL//2
            )
            circle(image, center, color=color, radius=R-30, feather=30)

    return image

H = 720
W = 1080
SHAPE = (H, W, 4)
COLORS = [
    # Blue, Green, Red
    (255, 0, 0),  # blue
    (0, 0, 255),  # red
    (0, 255, 0),  # green
    (255, 0, 160),  # purple
    (0, 145, 255),  # orange
    (255, 0, 255),  # pink
    (0, 255, 255),  # yellow
    (240, 230, 220),  # white
]

ROWS = 6
COLS = 8
RL = H // ROWS
CL = W // COLS
R = np.min((RL, CL)) // 2


if __name__ == "__main__":
    cv2.imshow('Image', full_color())
    cv2.waitKey(0)
