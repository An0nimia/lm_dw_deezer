from requests import get as req_get

from ..config.image import Image

from .data_utils import (
	DEFAULT_IMAGE_BYTES, DEFAULT_URL_TEMPLATE, DEFAULT_URL_IMAGE
)


def get_image_url(picture_md5: str, image: Image) -> str:
	cover_url = DEFAULT_URL_TEMPLATE.format(
		picture_md5 = picture_md5,
		width = image.width,
		height = image.height
	)

	return cover_url


def get_image(picture_md5: str, image: Image) -> tuple[bytes, str]:
	cover_url = DEFAULT_URL_IMAGE

	if picture_md5:
		cover_url = get_image_url(picture_md5, image)

		with req_get(cover_url, stream = True) as resp:
			image_bytes = resp.content
	else:
		image_bytes = DEFAULT_IMAGE_BYTES

	return image_bytes, cover_url