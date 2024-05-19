from dataclasses import dataclass

from ..config import QUALITY


type ITrack_Out = Track_Out | None


@dataclass
class Track_Out:
	path: str
	media_format: str
	quality: QUALITY
	quality_w: QUALITY