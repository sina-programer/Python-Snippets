import numpy as np
import cv2  # pip install opencv-python

def MSE(image1, image2):
    """ Calculate the similarity. (images must have exactly the same shape) """
    height, width = image1.shape
    diff = cv2.subtract(image1, image2)
    error = np.sum(diff ** 2)
    mse = error / (height * width)
    return mse

def similiraty(path1, path2, shape=(500, 500)):
    image1 = cv2.imread(path1)
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image1 = cv2.resize(image1, shape)

    image2 = cv2.imread(path2)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    image2 = cv2.resize(image2, shape)

    return MSE(image1, image2)
