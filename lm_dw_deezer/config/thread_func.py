from dataclasses import dataclass

from ..types.aliases import F_THREAD


@dataclass
class Thread_Func:
	func: F_THREAD
	WORKERS: int = 4