from api_deezer_full.gw.types import Track
from api_deezer_full.media.types import Media

from ..types.pipe_ext import (
	Album_Track as PIPE_Album_Track
)

from ..config import CONF
from ..types import DW_Album
from ..tagger import tagger_track

from ..types.aliases import (
	G_Track_Out, F_BE_DW
)

from .dws import dw_helper


def helper_album(
	gw_track_info: Track,
	media: Media,
	conf: CONF,
	pipe_track_info: PIPE_Album_Track,
	dir_name: str,
	album_info: DW_Album,
	func_be_dw: F_BE_DW
) -> G_Track_Out:

	track_out = dw_helper(
		track = gw_track_info,
		media = media,
		conf = conf,
		dir_name = dir_name,
		func_be_dw = func_be_dw
	)

	tagger_track(
		gw_info = gw_track_info,
		track_out = track_out,
		pipe_info = pipe_track_info,
		pipe_info_album = album_info.pipe_info,
		image_bytes = album_info.image_bytes
	)

	album_info.dw_tracks.append(track_out)

	yield track_out