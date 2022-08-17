from PIL import Image


def readImage(image_path: str) -> tuple:
    image_rgb = Image.open(image_path).convert("RGB")
    image_rgb_data = image_rgb.getdata()
    return image_rgb, list(image_rgb_data)


def readImageRgb(image_path: str) -> list:
    image_rgb_data = Image.open(image_path).convert("RGB").getdata()
    return image_rgb_data


def writeImage(new_image_data: list, rgb: Image, out_file_name: str) -> None:
    rgb.putdata(new_image_data)
    rgb.save(out_file_name)
