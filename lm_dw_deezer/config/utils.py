from api_deezer_full.media.types.aliases import (
	Media_Format, Format
)


from .enums import QUALITY


supported_fields_4_file: list[str] = [
	'title', 'artist', 'ISRC',
	'QUALITY', 'artists', 'album',
	'n_track', 'n_disk'
]


def create_media_json(media_formats: list[QUALITY]):
	return Media_Format(
		type = 'FULL',
		formats = [
			Format(
				cipher = 'BF_CBC_STRIPE',
				format = media_format
			)
			for media_format in media_formats
		]
	)


def __possible_save_formats(formats: list[str]) -> None:
	for a, f_format in enumerate(formats):
		print(f'{a}): {f_format}')


def possible_keyword_4_save_formats() -> None:
	__possible_save_formats(supported_fields_4_file)
