from collections.abc import Iterator

from api_deezer_full.gw.types import Track
from api_deezer_full.media.types import Media

from ..config import CONF
from ..tagger import tagger_track
from ..types.pipe_ext import Album_Track as PIPE_Album_Track

from ..types import (
	DW_Album, ITrack_Out
)

from .dws import (
	dw_helper, F_BE_DW
)


type G_DW_Album = Iterator[Helper_Album]
type G_Album = Iterator[DW_Album | Helper_Album]


class Helper_Album:
	def __init__(
		self,
		gw_track_info: Track,
		media: Media,
		conf: CONF,
		pipe_track_info: PIPE_Album_Track,
		dir_name: str,
		album_info: DW_Album,
		func_be_dw: F_BE_DW
	) -> None:

		self.gw_track_info = gw_track_info
		self.media = media
		self.conf = conf
		self.pipe_track_info = pipe_track_info
		self.dir_name = dir_name
		self.album_info = album_info
		self.func_be_dw = func_be_dw


	def dw_no_tag(self) -> ITrack_Out:
		track_out = dw_helper(
			track = self.gw_track_info,
			media = self.media,
			conf = self.conf,
			dir_name = self.dir_name,
			func_be_dw = self.func_be_dw
		)

		self.album_info.dw_tracks.append(track_out)

		return track_out


	def dw(self) -> ITrack_Out:
		track_out = self.dw_no_tag()

		tagger_track(
			gw_info = self.gw_track_info,
			track_out = track_out,
			pipe_info = self.pipe_track_info,
			pipe_info_album = self.album_info.pipe_info,
			image_bytes = self.album_info.image_bytes
		)

		return track_out