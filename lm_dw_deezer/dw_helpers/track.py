from collections.abc import Iterator

from api_deezer_full.media.types import Media

from ..config import CONF
from ..tagger import tagger_track
from ..types.pipe_ext import Track as PIPE_Track

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
		dw_track: DW_Track,
		media: Media,
		conf: CONF,
		dir_name: str,
		func_be_dw: F_BE_DW
	) -> None:

		self.dw_track = dw_track
		self.media = media
		self.conf = conf
		self.dir_name = dir_name
		self.func_be_dw = func_be_dw


	def dw_no_tag(self) -> ITrack_Out:
		track_out = dw_helper(
			track = self.dw_track.gw_info,
			media = self.media,
			conf = self.conf,
			dir_name = self.dir_name,
			func_be_dw = self.func_be_dw
		)

		self.dw_track.dw_track = track_out

		return track_out


	def dw(self) -> ITrack_Out:
		track_out = self.dw_no_tag()
		pipe_track: PIPE_Track = self.dw_track.pipe_info #pyright: ignore [reportAssignmentType]

		tagger_track(
			dw_track = self.dw_track,
			pipe_info_album = pipe_track.album,
			image_bytes = self.dw_track.image_bytes
		)

		return track_out