from api_deezer_full.gw.types import Track
from api_deezer_full.media.types import Media

from ..config import CONF
from ..tagger import tagger_track

from ..types.pipe_ext import Track as PIPE_Track

from ..types.aliases import (
	G_DW_Track, DW_Track, F_BE_DW
)

from .dws import dw_helper


def helper_playlist(
	gw_track_info: Track,
	media: Media,
	conf: CONF,
	pipe_track_info: PIPE_Track,
	dw_tracks: list[DW_Track],
	dir_name: str,
	func_be_dw: F_BE_DW
) -> G_DW_Track:


	track_out = dw_helper(
		track = gw_track_info,
		media = media,
		conf = conf,
		dir_name = dir_name,
		func_be_dw = func_be_dw
	)

	dw_track = DW_Track(
		image = conf.TRACKS_IMAGE,
		dw_track = track_out,
		gw_info = gw_track_info,
		pipe_info = pipe_track_info
	)

	tagger_track(
		gw_info = dw_track.gw_info,
		out = dw_track.dw_track,
		pipe_info = dw_track.pipe_info,
		pipe_info_album = dw_track.pipe_info.album,
		image_bytes = dw_track.image_bytes
	)

	dw_tracks.append(dw_track)

	yield dw_track