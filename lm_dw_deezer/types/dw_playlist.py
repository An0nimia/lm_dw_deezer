from dataclasses import (
	dataclass, field
)

from requests import get as req_get

from api_deezer_full.gw.types import Track as GW_Track

from .dw_track import DW_Tracks
from .data_utils import DEFAULT_URL_IMAGE
from .pipe_ext import Playlist as PIPE_Playlist


@dataclass
class DW_Playlist:
	pipe_info: PIPE_Playlist
	gw_tracks_info: list[GW_Track]
	dw_tracks: DW_Tracks = field(default_factory = list)
	zip_path: str | None = None


	def get_image_url(self) -> str:
		if not self.pipe_info.picture:
			return DEFAULT_URL_IMAGE

		return self.pipe_info.picture.url[0]


	def get_image(self) -> bytes:
		image = self.get_image_url()

		with req_get(image, stream = True) as resp:
			image_bytes = resp.content

		return image_bytes