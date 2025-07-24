from __future__ import annotations

from typing import (
	TYPE_CHECKING, TypedDict
)

from dataclasses import dataclass

from api_deezer_full.gw.types import Tracks_Track as GW_Track

if TYPE_CHECKING:
	from ..dw_helpers import Helper_T_Tracks

from .enums import DW_STATUS
from .dw_track import DW_Track
from .pipe_ext import Track as PIPE_Track


class STATUSES(TypedDict):
	helper: Helper_T_Tracks
	status: DW_STATUS
	dw_track: DW_Track


@dataclass
class DW_T_Tracks:
	gw_tracks_info: dict[int | str, GW_Track]
	pipe_tracks_info: dict[int | str, PIPE_Track]
	#dir_name: str
	#archive_path: str | None = None


	def __post_init__(self):
		self.info: dict[int | str, STATUSES] = {}

		for id_track in self.gw_tracks_info.keys():
			self.info[id_track] = STATUSES() #pyright: ignore [reportCallIssue] 
