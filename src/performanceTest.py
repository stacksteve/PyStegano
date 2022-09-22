# from SteganoWriter import SteganoWriter
from src.libStegano.SteganoReader import SteganoReader
from time import time
# from PIL import Image
# import cv2
from statistics import mean
from src.utils.PicReader import read_image_rgb, read_image_rgb_cv2


# WARNING: Use the value only if high performance is needed and the image has a higher resolution, otherwise
# error out of bounds possible
def readerTest():
    # Performance test for reading with standard seperator "!#!SepSepSep!#!" -> 136 or 135 best
    time_list = []
    time_dict = {}
    for i in range(1, 300):
        steg = SteganoReader("desktop.png", "desktop_secret.png")
        start = time()
        steg.extract_secret_message()
        time_needed = time() - start
        time_list.append(time_needed)
        time_dict[time_needed] = i

    time_list.sort()
    for i in range(10):
        print(f"{i + 1}.", time_list[i], end="\t\t\t")
        print(time_dict[time_list[i]])


def main():
    pass


if __name__ == '__main__':
    main()
