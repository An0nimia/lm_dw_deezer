from dataclasses import dataclass


type ITrack_Out = Track_Out | None


@dataclass
class Track_Out:
	path: str
	media_format: str
	quality: str
	quality_w: str