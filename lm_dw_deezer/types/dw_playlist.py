from __future__ import annotations

from typing import (
	TYPE_CHECKING, TypedDict
)

from dataclasses import (
	dataclass, field
)

from requests import get as req_get

from api_deezer_full.gw.types import Track as GW_Track

from ..utils import make_archive
from ..config.enums import COMPRESSION

if TYPE_CHECKING:
	from ..dw_helpers import Helper_Playlist

from .enums import DW_STATUS
from .dw_track import DW_Tracks
from .data_utils import DEFAULT_URL_IMAGE
from .pipe_ext import Playlist as PIPE_Playlist


class Helper(TypedDict):
	helper: Helper_Playlist
	status: DW_STATUS


@dataclass
class DW_Playlist:
	pipe_info: PIPE_Playlist
	gw_tracks_info: list[GW_Track]
	dir_name: str
	dw_tracks: DW_Tracks = field(default_factory = list)
	helpers: dict[str, Helper] = field(default_factory = dict)
	archive_path: str | None = None


	def get_image_url(self) -> str:
		if not self.pipe_info.picture:
			return DEFAULT_URL_IMAGE

		return self.pipe_info.picture.url[0]


	def get_image(self) -> bytes:
		image = self.get_image_url()

		with req_get(image, stream = True) as resp:
			image_bytes = resp.content

		return image_bytes


	def create_archive(self, type_arc: COMPRESSION) -> str:
		self.archive_path = make_archive(
			type_arc = type_arc,
			dir_name = self.dir_name,
			dw_tracks = self.dw_tracks
		)

		return self.archive_path