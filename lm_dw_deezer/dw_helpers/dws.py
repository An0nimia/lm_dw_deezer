from os.path import isfile

from collections.abc import Callable

from api_deezer_full.gw.types import Track
from api_deezer_full.media.types import Media

from ..config import (
	CONF, QUALITY
)

from ..decrypt.utils import gen_song_hash
from ..exceptions.no_stream_data import No_Stream_Data

from ..types import (
	ITrack_Out, Track_Out
)

from .utils import get_fn

from .utils_infos import (
	LEGACY_MEDIA_FORMAT, LEGACY_MEDIA_QUALITY
)


type F_BE_DW = Callable[
	[str, str, str], None
]


def dw_helper(
	track: Track,
	media: Media,
	conf: CONF,
	dir_name: str,
	func_be_dw: F_BE_DW
) -> ITrack_Out:

	track_out = None

	if media:
		media_format = 'mp3'

		if media.format == 'FLAC':
			media_format = 'flac'

		fn = get_fn(track, conf.FILE_FORMAT, media.format)

		path = f'{dir_name}/{fn}.{media_format}'

		track_out = Track_Out(
			path = path,
			media_format = media.media_type,
			quality = QUALITY.get_quality(media.format),
			quality_w = conf.QUALITIES[0],
		)

		if isfile(track_out.path) and not conf.RE_DOWNLOAD:
			return track_out

		id_track = track.fallback.id if track.fallback else track.id

		func_be_dw(id_track, media.sources[0].url, track_out.path)
	else:
		if conf.LEGACY_DOWNLOAD_RECURSION:
			track_out = dw_helper_legacy(
				track = track,
				conf = conf,
				dir_name = dir_name,
				func_be_dw = func_be_dw
			)

	return track_out


def dw_helper_legacy(
	track: Track,
	conf: CONF,
	dir_name: str,
	func_be_dw: F_BE_DW
) -> ITrack_Out:

	fn = get_fn(track, conf.FILE_FORMAT, LEGACY_MEDIA_QUALITY)

	path = f'{dir_name}/{fn}.{LEGACY_MEDIA_FORMAT}'

	track_out = Track_Out(
		path = path,
		media_format = LEGACY_MEDIA_FORMAT,
		quality = QUALITY.OK,
		quality_w = conf.QUALITIES[0]
	)

	if isfile(track_out.path) and not conf.RE_DOWNLOAD:
		return track_out

	track_md5 = track.md5_origin
	id_track = track.id
	media_version = track.media_version

	if track.fallback:
		id_track = track.fallback.id
		track_md5 = track.fallback.md5_origin
		media_version = track.fallback.media_version

	dw_url = gen_song_hash(track_md5, LEGACY_MEDIA_QUALITY, id_track, media_version)

	try:
		func_be_dw(id_track, dw_url, track_out.path)
	except No_Stream_Data:
		track_out = None

	return track_out