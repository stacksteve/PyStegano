from enum import Enum
from PIL import Image


class ImageFormat(Enum):
    PNG = 0
    JPG = JPEG = 1
    PPM = 2


def detectFormat(image_path: str) -> ImageFormat:
    image_format = image_path.split(".")[-1].upper()
    return ImageFormat[image_format].value


def readImageData(image_path: str) -> tuple:
    image_rgb = Image.open(image_path).convert("RGB")
    image_rgb_data = image_rgb.getdata()
    return image_rgb, image_rgb_data


def writeImage() -> None:
    pass


def main():
    print(detectFormat("test.png"))


if __name__ == '__main__':
    main()
