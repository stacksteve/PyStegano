from PIL import Image


def read_image(image_path: str) -> tuple:
    image_rgb = Image.open(image_path).convert("RGB")
    image_rgb_data = image_rgb.getdata()
    return image_rgb, list(image_rgb_data)


def read_image_rgb(image_path: str) -> list:
    return Image.open(image_path).convert("RGB").getdata()


def write_image(new_image_data: list, pil_image: Image, out_file_name: str) -> None:
    pil_image.putdata(new_image_data)
    pil_image.save(out_file_name)
