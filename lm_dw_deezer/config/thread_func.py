from threading import Event
from dataclasses import dataclass
from collections.abc import Callable

from typing import TYPE_CHECKING


if TYPE_CHECKING:
	from ..dw_helpers import Helper_Album, Helper_Playlist


type F_THREAD = Callable[
	[Event, Helper_Album | Helper_Playlist], None
]

@dataclass
class Thread_Func:
	func: F_THREAD
	WORKERS: int = 4