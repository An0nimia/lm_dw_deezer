from __future__ import annotations

from typing import (
	TYPE_CHECKING, TypedDict
)

from dataclasses import (
	dataclass, field
)

from api_deezer_full.gw.types import Track as GW_Track

from ..config.enums import COMPRESSION

from ..medjays import (
	DW_Medjay, Event
)

from ..config import (
	Thread_Func, Image
)

if TYPE_CHECKING:
	from ..dw_helpers import Helper_Album

from .enums import DW_STATUS
from .dw_track import DW_Tracks
from .utils_image import get_image
from .pipe_ext import Album as PIPE_Album

from .utils import (
	wait_threads, make_archive
)


class STATUSES(TypedDict):
	helper: Helper_Album
	status: DW_STATUS


@dataclass
class DW_Album:
	image: Image
	gw_tracks_info: list[GW_Track]
	pipe_info: PIPE_Album
	dir_name: str
	statuses: dict[str, STATUSES] = field(default_factory = dict)
	dw_tracks: DW_Tracks = field(default_factory = list)
	archive_path: str | None = None

	image_bytes: bytes = field(
		init = False,
		repr = False
	)


	def __post_init__(self):
		self.cover = self.gw_tracks_info[0].album_picture_md5
		self.image_bytes, self.cover_url = get_image(self.cover, self.image)


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
			self.statuses[track]['helper']

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