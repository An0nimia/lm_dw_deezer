from os.path import isfile

from api_deezer_full.gw.types import Track
from api_deezer_full.media.types import Media

from ..config import CONF
from ..decrypt.utils import gen_song_hash

from ..types.aliases import (
	ITrack_Out, Track_Out, F_BE_DW
)

from .utils import get_fn


__LEGACY_MEDIA_FORMAT = 'mp3'
__LEGACY_MEDIA_QUALITY = 'MP3_128'


def dw_helper(
	track: Track,
	media: Media,
	conf: CONF,
	dir_name: str,
	func_be_dw: F_BE_DW
) -> ITrack_Out:

	dw_track = None

	if not media is None:
		media_format = 'mp3'

		if media.format == 'FLAC':
			media_format = 'flac'

		fn = get_fn(track, conf.FILE_FORMAT, media.format)

		path = f'{dir_name}/{fn}.{media_format}'

		dw_track = Track_Out(
			path = path,
			media_format = media.media_type,
			quality = media.format,
			quality_w = conf.QUALITIES[0],
		)

		if isfile(dw_track.path) and not conf.RE_DOWNLOAD:
			return dw_track

		id_track = track.fallback.id if track.fallback else track.id

		func_be_dw(id_track, media.sources[0].url, dw_track.path)
	else:
		dw_track = dw_helper_legacy(
			track, conf, dir_name, func_be_dw
		)

	return dw_track


def dw_helper_legacy(
	track: Track,
	conf: CONF,
	dir_name: str,
	func_be_dw: F_BE_DW
) -> ITrack_Out:
	fn = get_fn(track, conf.FILE_FORMAT, __LEGACY_MEDIA_QUALITY)

	path = f'{dir_name}/{fn}.{__LEGACY_MEDIA_FORMAT}'

	dw_track = Track_Out(
		path = path,
		media_format = __LEGACY_MEDIA_FORMAT,
		quality = __LEGACY_MEDIA_QUALITY,
		quality_w = conf.QUALITIES[0]
	)

	if isfile(dw_track.path) and not conf.RE_DOWNLOAD:
		return dw_track

	track_md5 = track.md5_origin
	id_track = track.id
	media_version = track.media_version

	if track.fallback:
		id_track = track.fallback.id
		track_md5 = track.fallback.md5_origin
		media_version = track.fallback.media_version

	dw_url = gen_song_hash(track_md5, __LEGACY_MEDIA_QUALITY, id_track, media_version)
	func_be_dw(id_track, dw_url, dw_track.path)

	return dw_track