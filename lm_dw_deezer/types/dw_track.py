from dataclasses import (
	dataclass, field
)

from api_deezer_full.gw.types import Track as GW_Track

from ..config.image import Image

from .utils import get_image
from .track_out import ITrack_Out
from .pipe_ext import Track as PIPE_Track


type DW_Tracks = list[DW_Track]


@dataclass
class DW_Track:
	image: Image
	gw_info: GW_Track
	pipe_info: PIPE_Track
	dw_track: ITrack_Out = None

	image_bytes: bytes = field(
		init = False,
		repr = False
	)


	def __post_init__(self):
		self.cover = self.gw_info.album_picture_md5
		self.image_bytes, self.cover_url = get_image(self.cover, self.image)