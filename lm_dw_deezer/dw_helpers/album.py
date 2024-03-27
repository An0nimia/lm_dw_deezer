from collections.abc import Iterator

from api_deezer_full.gw.types import Track
from api_deezer_full.media.types import Media

from ..config import CONF
from ..tagger import tagger_track
from ..types.enums import DW_STATUS
from ..types.pipe_ext import Album_Track as PIPE_Album_Track

from ..types import (
	DW_Album, DW_Track, ITrack_Out
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
		album_info: DW_Album,
		func_be_dw: F_BE_DW
	) -> None:

		self.gw_track_info = gw_track_info
		self.media = media
		self.conf = conf
		self.pipe_track_info = pipe_track_info
		self.album_info = album_info
		self.func_be_dw = func_be_dw


	def just_metadata(self) -> DW_Track:
		self.dw_track = DW_Track(
			image = self.conf.TRACK_IMAGE,
			gw_info = self.gw_track_info,
			pipe_info = self.pipe_track_info
		)

		self.album_info.dw_tracks.append(self.dw_track)

		return self.dw_track


	def dw_no_tag(self) -> ITrack_Out:
		self.just_metadata()

		track_out = dw_helper(
			track = self.gw_track_info,
			media = self.media,
			conf = self.conf,
			dir_name = self.album_info.dir_name,
			func_be_dw = self.func_be_dw
		)

		if track_out:
			self.album_info.statuses[self.gw_track_info.id]['status'] = DW_STATUS.DOWNLOADED
		else:
			self.album_info.statuses[self.gw_track_info.id]['status'] = DW_STATUS.UN_DOWNLABLE

		self.dw_track.dw_track = track_out

		return track_out


	def dw(self) -> ITrack_Out:
		track_out = self.dw_no_tag()

		tagger_track(
			pipe_info_album = self.album_info.pipe_info,
			dw_track = self.dw_track,
			image_bytes = self.album_info.image_bytes
		)

		return track_out