"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""
import argparse

import cv2
import numpy as np


colors = {
    (0,0,0) : '30', # Black
    (128,0,0) :  '31', # Red
    (0,128,0) : '32', # Green
    (128,128,0):    '33', # Yellow
    (0,0,128):    '34', # Blue
    (128,0,128):    '35', # Magenta
    (0,128,128):    '36', # Cyan
    (128,128,128):    '37', # Light gray
    (64,64,64):    '90', # Dark gray
    (256,0,0):    '91', # Light red
    (0,256,0):    '92', # Light green
    (256,256,0):    '93', # Light yellow
    (0,0,256):    '94', # Light blue
    (256,0,256):    '95', # Light magenta
    (0,256,256):    '96', # Light cyan
    (256,256,256):    '97', # White
}

def colorize_string(string, color):
    return '\033[' + colors[color] + 'm' + string

def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="data/output.txt", help="Path to output text file")
    parser.add_argument("--mode", type=str, default="complex", choices=["simple", "complex"],
                        help="10 or 70 different characters")
    parser.add_argument("--num_cols", type=int, default=150, help="number of character for output's width")
    parser.add_argument("--color", type=bool, default=False, help="Whether the output should use bash colors")
    args = parser.parse_args()
    return args


def main(opt):

    if opt.mode == "simple":
        CHAR_LIST = '@%#*+=-:. '
    else:
        CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    num_chars = len(CHAR_LIST)
    num_cols = opt.num_cols
    image = cv2.imread(opt.input)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray_image.shape
    cell_width = width / opt.num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    output_file = open(opt.output, 'w')
    for i in range(num_rows):
        for j in range(num_cols):
            index = min(int(np.mean(gray_image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                                         int(j * cell_width):min(int((j + 1) * cell_width),
                                                                width)]) * num_chars / 255), num_chars - 1)
            char = CHAR_LIST[index]
            if opt.color:
                bgr_mean = np.mean(image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                                      int(j * cell_width):min(int((j + 1) * cell_width), width)], axis=(0,1))
                mean_b, mean_g, mean_r = bgr_mean
                min_dist = 256 * 256 * 256
                color = None

                for k in colors.keys():
                    r,g,b = k
                    distance = (mean_b - b) * (mean_b - b) + (mean_g - g) * (mean_g - g) + (mean_r - r) * (mean_r - r)
                    if distance < min_dist:
                        min_dist = distance
                        color = k

                char = colorize_string(char, color)

            output_file.write(char)
        output_file.write("\n")
    output_file.close()


if __name__ == '__main__':
    opt = get_args()
    main(opt)
