from dataclasses import (
	dataclass, field
)

from .dw_track import DW_Tracks
from .pipe_ext import Playlist as PIPE_Playlist


@dataclass
class DW_Playlist:
	pipe_info: PIPE_Playlist
	dw_tracks: DW_Tracks = field(default_factory = list)
	zip_path: str | None = None