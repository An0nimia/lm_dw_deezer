from .data_utils import (
	DEFAULT_FILE_FORMATS, DEFAULT_FOLDER_FORMATS, QUALITS
)


def create_media_json(media_formats: list[QUALITS]):
	media_json = {
		'type': 'FULL',
		'formats': [
			{
				'cipher': 'BF_CBC_STRIPE',
				'format': media_format
			}
			for media_format in media_formats
		]
	}

	return media_json


def __possible_save_formats(formats: list[str]) -> None:
	for a, f_format in enumerate(formats):
		print(f'{a}): {f_format}')


def possible_fn_save_formats() -> None:
	__possible_save_formats(DEFAULT_FILE_FORMATS)


def possible_dirs_save_formats() -> None:
	__possible_save_formats(DEFAULT_FOLDER_FORMATS)