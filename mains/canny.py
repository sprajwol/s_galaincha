import os
import sys
import time

from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matlab.engine

from .sobel import sobel_edge_detection
from .gaussian_smoothing import gaussian_blur
from s_galaincha.settings import PROJECT_ROOT


def threshold(image, low, high, weak):
    output = np.zeros(image.shape)

    strong = 255

    strong_row, strong_col = np.where(image >= high)
    weak_row, weak_col = np.where((image <= high) & (image >= low))

    output[strong_row, strong_col] = strong
    output[weak_row, weak_col] = weak

    return output


def hysteresis(image, weak):
    image_row, image_col = image.shape
    top_to_bottom = image.copy()

    for row in range(1, image_row):
        for col in range(1, image_col):
            if top_to_bottom[row, col] == weak:
                if top_to_bottom[row, col + 1] == 255 or top_to_bottom[row, col - 1] == 255 or top_to_bottom[row - 1, col] == 255 or top_to_bottom[
                        row + 1, col] == 255 or top_to_bottom[
                        row - 1, col - 1] == 255 or top_to_bottom[row + 1, col - 1] == 255 or top_to_bottom[row - 1, col + 1] == 255 or top_to_bottom[
                        row + 1, col + 1] == 255:
                    top_to_bottom[row, col] = 255
                else:
                    top_to_bottom[row, col] = 0

    bottom_to_top = image.copy()

    for row in range(image_row - 1, 0, -1):
        for col in range(image_col - 1, 0, -1):
            if bottom_to_top[row, col] == weak:
                if bottom_to_top[row, col + 1] == 255 or bottom_to_top[row, col - 1] == 255 or bottom_to_top[row - 1, col] == 255 or bottom_to_top[
                        row + 1, col] == 255 or bottom_to_top[
                        row - 1, col - 1] == 255 or bottom_to_top[row + 1, col - 1] == 255 or bottom_to_top[row - 1, col + 1] == 255 or bottom_to_top[
                        row + 1, col + 1] == 255:
                    bottom_to_top[row, col] = 255
                else:
                    bottom_to_top[row, col] = 0

    right_to_left = image.copy()

    for row in range(1, image_row):
        for col in range(image_col - 1, 0, -1):
            if right_to_left[row, col] == weak:
                if right_to_left[row, col + 1] == 255 or right_to_left[row, col - 1] == 255 or right_to_left[row - 1, col] == 255 or right_to_left[
                        row + 1, col] == 255 or right_to_left[
                        row - 1, col - 1] == 255 or right_to_left[row + 1, col - 1] == 255 or right_to_left[row - 1, col + 1] == 255 or right_to_left[
                        row + 1, col + 1] == 255:
                    right_to_left[row, col] = 255
                else:
                    right_to_left[row, col] = 0

    left_to_right = image.copy()

    for row in range(image_row - 1, 0, -1):
        for col in range(1, image_col):
            if left_to_right[row, col] == weak:
                if left_to_right[row, col + 1] == 255 or left_to_right[row, col - 1] == 255 or left_to_right[row - 1, col] == 255 or left_to_right[
                        row + 1, col] == 255 or left_to_right[
                        row - 1, col - 1] == 255 or left_to_right[row + 1, col - 1] == 255 or left_to_right[row - 1, col + 1] == 255 or left_to_right[
                        row + 1, col + 1] == 255:
                    left_to_right[row, col] = 255
                else:
                    left_to_right[row, col] = 0

    final_image = top_to_bottom + bottom_to_top + right_to_left + left_to_right

    final_image[final_image > 255] = 255

    return final_image


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def non_max_suppression(gradient_magnitude, gradient_direction):
    image_row, image_col = gradient_magnitude.shape

    output = np.zeros(gradient_magnitude.shape)

    PI = 180

    for row in range(1, image_row - 1):
        for col in range(1, image_col - 1):
            direction = gradient_direction[row, col]

            # (0 - PI/8 and 15PI/8 - 2PI)
            if (0 <= direction < PI / 8) or (15 * PI / 8 <= direction <= 2 * PI):
                before_pixel = gradient_magnitude[row, col - 1]
                after_pixel = gradient_magnitude[row, col + 1]

            elif (PI / 8 <= direction < 3 * PI / 8) or (9 * PI / 8 <= direction < 11 * PI / 8):
                before_pixel = gradient_magnitude[row + 1, col - 1]
                after_pixel = gradient_magnitude[row - 1, col + 1]

            elif (3 * PI / 8 <= direction < 5 * PI / 8) or (11 * PI / 8 <= direction < 13 * PI / 8):
                before_pixel = gradient_magnitude[row - 1, col]
                after_pixel = gradient_magnitude[row + 1, col]

            else:
                before_pixel = gradient_magnitude[row - 1, col - 1]
                after_pixel = gradient_magnitude[row + 1, col + 1]

            if gradient_magnitude[row, col] >= before_pixel and gradient_magnitude[row, col] >= after_pixel:
                output[row, col] = gradient_magnitude[row, col]

    return output


def inverte(imagem):
    imagem = (255-imagem)
    return imagem


def mainpart(filename, inurl, outurl):
    """Reading an image"""
    input_file = inurl + filename
    infile = open(input_file, "rb")
    in_image = Image.open(infile)
    """Canny Edge Detection process started"""
    """STEP 1:Converting to GRAYSCALE"""
    in_image = in_image.convert("L")
    """Getting image pixels data in list form"""
    image_list = list(in_image.getdata())
    """Getting image attributes from image"""
    xlength, ylength = in_image.size
    file, ext = os.path.splitext(filename)
    print(file, "a", ext)
    """Reshaping image pixels in (xlength,ylength) array"""
    original_gray = np.reshape(np.array(image_list), (ylength, xlength))

    """STEP 2:Gaussian Kernel Filter"""
    blurred_image = gaussian_blur(original_gray, kernel_size=9)

    """STEP 3:Sobel Edge Detection and Non-Maximum Suppression"""
    edge_filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    # direct blue nagari pathako image lai baru front end maa gaussian blur garne ki nagarne vanne option halnu parla
    gradient_magnitude, gradient_direction = sobel_edge_detection(
        original_gray, edge_filter, convert_to_degree=True)
    sobel_n_nonmax = non_max_suppression(
        gradient_magnitude, gradient_direction)

    """STEP 4:Double Thresholding"""
    weak = 200
    double_thresholding = threshold(sobel_n_nonmax, 5, 20, weak=weak)

    """STEP 5:Hysteris"""
    hysteresis_image = hysteresis(double_thresholding, weak)
    """Canny Edge Detection process ended"""
    """DILATED & ERODED"""

    for x in range(xlength):
        for y in range(ylength):
            if x == 0 or x == (xlength-1) or y == 0 or y == (ylength-1):
                hysteresis_image[y, x] = 255
            else:
                continue
    dialted_image = cv2.dilate(hysteresis_image, None, iterations=2)
    dialted_image = cv2.erode(dialted_image, None, iterations=1)
    """INVERT IMAGE"""
    # image = cv2.imread(new_file)
    inverted_image = dialted_image

    """SAVE INVERT IMAGE"""
    inverted_image_list = np.reshape(
        inverted_image, (xlength*ylength,)).tolist()
    new_file = "A7_" + file + ext
    onlyfile = "A7_" + file
    az = PROJECT_ROOT + "\\"
    az_url = az + outurl + new_file
    # + outurl + new_file
    print("AZ", az_url)
    try:
        output_image = Image.new(in_image.mode, in_image.size, None)
        output_image.putdata(inverted_image_list)
        output_image.save(az_url, in_image.format)
    except(IOError):
        print("Output file error1:")

    # TODO: detect the shape and calculate area
    # """import matlab.engine ko ho not working"""
    eng = matlab.engine.start_matlab()
    txt, aaa = eng.shapee(az, outurl, new_file, onlyfile, nargout=2)
    print(txt)
    print(aaa)
    """Making image on every step"""
    """STEP 1:Converting to GRAYSCALE"""
    original_gray_list = np.reshape(original_gray, (xlength*ylength,)).tolist()
    new_file = "A1_" + file + ext
    try:
        output_image = Image.new(in_image.mode, in_image.size, None)
        output_image.putdata(original_gray_list)
        output_image.save(new_file, in_image.format)
    except(IOError):
        print("Output file error2:")
    """STEP 2:Gaussian Kernel Filter"""
    blurred_image_list = np.reshape(blurred_image, (xlength*ylength,)).tolist()
    new_file = "A2_" + file + ext
    try:
        output_image = Image.new(in_image.mode, in_image.size, None)
        output_image.putdata(blurred_image_list)
        output_image.save(new_file, in_image.format)
    except(IOError):
        print("Output file error3:")
    """STEP 3:Sobel Edge Detection and Non-Maximum Suppression"""
    sobel_n_nonmax_list = np.reshape(
        sobel_n_nonmax, (xlength*ylength,)).tolist()
    new_file = "A3_" + file + ext
    try:
        output_image = Image.new(in_image.mode, in_image.size, None)
        output_image.putdata(sobel_n_nonmax_list)
        output_image.save(new_file, in_image.format)
    except(IOError):
        print("Output file error4:")
    """STEP 4:Double Thresholding"""
    double_thresholding_list = np.reshape(
        double_thresholding, (xlength*ylength,)).tolist()
    new_file = "A4_" + file + ext
    try:
        output_image = Image.new(in_image.mode, in_image.size, None)
        output_image.putdata(double_thresholding_list)
        output_image.save(new_file, in_image.format)
    except(IOError):
        print("Output file error5:")
    """STEP 5:Hysteris"""
    hysteresis_image_list = np.reshape(
        hysteresis_image, (xlength*ylength,)).tolist()
    new_file = "A5_" + file + ext
    try:
        output_image = Image.new(in_image.mode, in_image.size, None)
        output_image.putdata(hysteresis_image_list)
        output_image.save(new_file, in_image.format)
    except(IOError):
        print("Output file error6:")
    """DILATED & ERODED"""
    dialted_image_list = np.reshape(
        dialted_image, (xlength*ylength,)).tolist()
    new_file = "A6_" + file + ext
    try:
        output_image = Image.new(in_image.mode, in_image.size, None)
        output_image.putdata(dialted_image_list)
        output_image.save(new_file, in_image.format)
    except(IOError):
        print("Output file error7:")

    return txt, aaa
