from collections.abc import Iterator

from api_deezer_full.media.types import Media

from ..config import CONF
from ..tagger import tagger_track

from ..types import (
	DW_Track, ITrack_Out
)

from .dws import (
	dw_helper, F_BE_DW
)


type G_DW_Track = Iterator[Helper_Track]
type G_Track = Iterator[DW_Track | Helper_Track]


class Helper_Track:
	def __init__(
		self,
		track_info: DW_Track,
		media: Media,
		conf: CONF,
		dir_name: str,
		func_be_dw: F_BE_DW
	) -> None:

		self.track_info = track_info
		self.media = media
		self.conf = conf
		self.dir_name = dir_name
		self.func_be_dw = func_be_dw


	def dw_no_tag(self) -> ITrack_Out:
		track_out = dw_helper(
			track = self.track_info.gw_info,
			media = self.media,
			conf = self.conf,
			dir_name = self.dir_name,
			func_be_dw = self.func_be_dw
		)

		self.track_info.dw_track = track_out

		return track_out


	def dw(self) -> ITrack_Out:
		dw_track = self.dw_no_tag()

		tagger_track(
			gw_info = self.track_info.gw_info,
			track_out = self.track_info.dw_track,
			pipe_info = self.track_info.pipe_info,
			pipe_info_album = self.track_info.pipe_info.album,
			image_bytes = self.track_info.image_bytes
		)

		return dw_track