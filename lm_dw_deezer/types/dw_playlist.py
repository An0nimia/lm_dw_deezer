from __future__ import annotations

from typing import (
	TYPE_CHECKING, TypedDict
)

from dataclasses import (
	dataclass, field
)

from requests import get as req_get

from api_deezer_full.gw.types import Track as GW_Track

from ..medjays import (
	DW_Medjay, Event
)

from ..config import Thread_Func
from ..config.enums import COMPRESSION

if TYPE_CHECKING:
	from ..dw_helpers import Helper_Playlist

from .enums import DW_STATUS
from .dw_track import DW_Tracks

from .utils import (
	wait_threads, make_archive
)

from .data_utils import DEFAULT_URL_IMAGE
from .pipe_ext import Playlist as PIPE_Playlist


class STATUSES(TypedDict):
	helper: Helper_Playlist
	status: DW_STATUS


@dataclass
class DW_Playlist:
	pipe_info: PIPE_Playlist
	gw_tracks_info: list[GW_Track]
	dir_name: str
	dw_tracks: DW_Tracks = field(default_factory = list)
	statuses: dict[str, STATUSES] = field(default_factory = dict)
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


	def get_undownloaded(self) -> filter[str]:
		return filter(
			lambda track: self.statuses[track]['status'] == DW_STATUS.NOT_DOWNLOADED,
			self.statuses
		)


	def download_undownloaded(self) -> None:
		for track in self.get_undownloaded():
			self.statuses[track]['helper'].dw()


	def download_undownloaded_thread(self, thread_func: Thread_Func) -> None:
		threads: list[DW_Medjay] = []
		event = Event()
		workers = thread_func.WORKERS

		for track in self.get_undownloaded():
			if workers == 0:
				wait_threads(threads)

				if event.is_set():
					break

				workers = thread_func.WORKERS

			c_thread = DW_Medjay(
				target = thread_func.func,
				args = (self.statuses[track]['helper'],),
				event = event
			)

			c_thread.start()
			threads.append(c_thread)
			workers -= 1

		wait_threads(threads)


	def download_undownloaded_w_archive(self, type_arc: COMPRESSION) -> str:
		self.download_undownloaded()

		return self.create_archive(type_arc)


	def download_undownloaded_thread_w_archive(self, thread_func: Thread_Func, type_arc: COMPRESSION) -> str:
		self.download_undownloaded_thread(thread_func)

		return self.create_archive(type_arc)