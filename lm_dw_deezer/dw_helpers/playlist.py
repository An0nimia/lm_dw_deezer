from collections.abc import Iterator

from api_deezer_full.gw.types import Track
from api_deezer_full.media.types import Media

from ..config import CONF
from ..tagger import tagger_track
from ..types.pipe_ext import Track as PIPE_Track

from ..types import (
	DW_Track, DW_Playlist, ITrack_Out
)

from .dws import (
	dw_helper, F_BE_DW
)


type G_DW_Playlist = Iterator[Helper_Playlist]
type G_Playlist = Iterator[DW_Playlist | Helper_Playlist]


class Helper_Playlist:
	def __init__(
		self,
		gw_track_info: Track,
		media: Media,
		conf: CONF,
		pipe_track_info: PIPE_Track,
		dw_tracks: list[DW_Track],
		dir_name: str,
		func_be_dw: F_BE_DW
	) -> None:

		self.gw_track_info = gw_track_info
		self.media = media
		self.conf = conf
		self.pipe_track_info = pipe_track_info
		self.dir_name = dir_name
		self.dw_tracks = dw_tracks
		self.func_be_dw = func_be_dw


	def just_metadata(self) -> None:
		self.dw_track = DW_Track(
			image = self.conf.TRACK_IMAGE,
			gw_info = self.gw_track_info,
			pipe_info = self.pipe_track_info
		)

		self.dw_tracks.append(self.dw_track)


	def dw_no_tag(self) -> ITrack_Out:
		self.just_metadata()

		track_out = dw_helper(
			track = self.gw_track_info,
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