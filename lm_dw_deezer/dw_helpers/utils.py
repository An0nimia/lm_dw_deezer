from os import makedirs

from api_deezer_full.gw.types import (
	Track, Artists
)

from ..config import CONF


def artists_2_str(artists: Artists):
	return '│'.join(
		artist.name
		for artist in artists
	)


def __excape_unwanted(fn: str) -> str:
	# https://www.unicode.org/Public/security/latest/confusables.txt

	fn = (
		fn
		.replace('/', '᜵')
		.replace('?', 'ʔ')
		.replace('#', '')
		.replace('%', '٪')
		.replace('&', 'ꝸ')
		.replace('$', '🄏')
		.replace('!', 'ǃ')
		.replace('@', '')
		.replace('"', '᳓')
		.replace('\'', '᳓')
		.replace(':', '∶')
		.replace('+', '᛭')
		.replace('|', '│')
		.replace('=', '᐀')
		.replace('\\', '⧵')
		.replace('`', '՝')
		.replace('*', '⁎')
	)

	return fn


def get_fn(
	track: Track,
	s: str,
	quality: str
) -> str:

	fn = s.format(
		title = f'{track.title}{track.version}',
		artist = track.artists[0].name,
		ISRC = track.ISRC,
		QUALITY = quality,
		artists = artists_2_str(track.artists),
		album = track.album_title,
		n_track = track.track_number,
		n_disk = track.disk_number
	)

	return __excape_unwanted(fn)


def create_dir_w_track(conf: CONF, track: Track) -> str:
	dir_name = get_fn(track, conf.FOLDER_FORMAT, '')
	dir_name = f'{conf.OUTPUT_FOLDER}/{dir_name}'
	makedirs(dir_name, exist_ok = True)

	return dir_name


def create_dir(conf: CONF, name: str) -> str:
	dir_name = __excape_unwanted(name)
	dir_name = f'{conf.OUTPUT_FOLDER}/{dir_name}'
	makedirs(dir_name, exist_ok = True)

	return dir_name