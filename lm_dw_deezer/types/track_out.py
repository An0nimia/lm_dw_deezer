from dataclasses import dataclass


type ITrack_Out = Track_Out | None
type ITracks_Out = list[ITrack_Out]


@dataclass
class Track_Out:
	path: str
	media_format: str
	quality: str
	quality_w: str