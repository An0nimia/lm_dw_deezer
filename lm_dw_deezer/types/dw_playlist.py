from dataclasses import (
	dataclass, field
)

from .dw_track import DW_Track
from .pipe_ext import Playlist as PIPE_Playlist


type DW_Tracks = list[DW_Track]


@dataclass
class DW_Playlist:
	pipe_info: PIPE_Playlist
	dw_tracks: DW_Tracks = field(default_factory = list)
	zip_path: str | None = None