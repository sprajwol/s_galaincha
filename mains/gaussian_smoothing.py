import numpy as np
import matplotlib.pyplot as plt
import math
import cv2
from .convolution import convolution


def dnorm(x, mu, sd):
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)


def gaussian_kernel(size, sigma=1):
    kernel_1D = np.linspace(-(size // 2), size // 2, size)
    for i in range(size):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)

    kernel_2D *= 1.0 / kernel_2D.max()

    return kernel_2D


def gaussian_blur(image, kernel_size):
    kernel = gaussian_kernel(
        kernel_size, sigma=math.sqrt(kernel_size))
    blured = convolution(image, kernel, average=True)
    cv2.imwrite('01.png', blured)
    plt.imshow(blured, cmap='gray')
    plt.savefig('blured.png')
    # plt.show()

    return blured
