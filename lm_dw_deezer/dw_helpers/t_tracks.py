from collections.abc import Iterator

from dataclasses import dataclass

from api_deezer_full.gw.types import Track
from api_deezer_full.media.types import Media

from ..config import CONF
from ..tagger import tagger_track
from ..types.enums import DW_STATUS
from ..types.pipe_ext import Track as PIPE_Track

from ..types import (
	DW_T_Tracks, DW_Track, ITrack_Out
)

from .dws import (
	dw_helper, F_BE_DW
)


type G_DW_T_Tracks = Iterator[Helper_T_Tracks]
type G_T_Tracks = Iterator[DW_T_Tracks | Helper_T_Tracks]


@dataclass
class Helper_T_Tracks:
	gw_track_info: Track
	pipe_track_info: PIPE_Track
	media: Media
	conf: CONF
	t_tracks_info: DW_T_Tracks
	func_be_dw: F_BE_DW


	def just_metadata(self) -> DW_Track:
		self.dw_track = DW_Track(
			image = self.conf.TRACK_IMAGE,
			gw_info = self.gw_track_info,
			pipe_info = self.pipe_track_info
		)

		self.t_tracks_info.info[self.gw_track_info.id]['dw_track'] = self.dw_track

		return self.dw_track


	def dw_no_tag(self) -> ITrack_Out:
		self.just_metadata()

		track_out = dw_helper(
			track = self.gw_track_info,
			media = self.media,
			conf = self.conf,
			dir_name = self.conf.OUTPUT_FOLDER,
			func_be_dw = self.func_be_dw
		)

		if track_out:
			self.t_tracks_info.info[self.gw_track_info.id]['status'] = DW_STATUS.DOWNLOADED
		else:
			self.t_tracks_info.info[self.gw_track_info.id]['status'] = DW_STATUS.UN_DOWNLABLE

		self.dw_track.dw_track = track_out

		return track_out


	def dw(self) -> ITrack_Out:
		track_out = self.dw_no_tag()

		tagger_track(
			dw_track = self.dw_track,
			pipe_info_album = self.pipe_track_info.album,
			image_bytes = self.dw_track.image_bytes
		)

		return track_out
