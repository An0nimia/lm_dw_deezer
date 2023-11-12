from dataclasses import (
	dataclass, field
)

from api_deezer_full.gw.types import Track as GW_Track

from ..config.image import Image

from .utils import get_image
from .dw_track import ITrack_Out
from .pipe_ext.album import Album as PIPE_Album


type ITracks_Out = list[ITrack_Out]


@dataclass
class DW_Album:
	image: Image
	gw_tracks_info: list[GW_Track]
	pipe_info: PIPE_Album
	dw_tracks: ITracks_Out = field(default_factory = list)
	zip_path: str | None = None

	image_bytes: bytes = field(
		init = False,
		repr = False
	)


	def __post_init__(self):
		self.cover = self.gw_tracks_info[0].album_picture_md5
		self.image_bytes, self.cover_url = get_image(self.cover, self.image)