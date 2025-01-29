import base64
import io

import PIL.Image

from core.logging import logger


def save(image: PIL.Image, file_path: str) -> None:
    logger.debug(f"Saving image to {file_path}")
    with open(file=file_path, mode="w") as file:
        image.save(file)


def get(file_path: str) -> PIL.Image:
    logger.debug(f"Getting image from {file_path}")
    return PIL.Image.open(file_path, mode="r")


def from_base64(image: str) -> PIL.Image:
    buff = io.BytesIO(base64.b64decode(image))
    image_decoded = PIL.Image.open(buff)
    logger.debug(f"Decoded image")
    return image_decoded


def to_base64(image: PIL.Image, format: str = "png") -> str:
    buff = io.BytesIO()
    image.save(buff, format=format.upper())
    image_encoded = base64.b64encode(buff.getvalue()).decode()
    logger.debug(f"Encoded {format} image")
    return image_encoded
