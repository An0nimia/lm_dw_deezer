from typing import Any

from threading import (
	Thread, Event
)

from collections.abc import (
	Callable, Iterable, Mapping
)


class DW_Medjay(Thread):
	def __init__(
		self,
		group: None = None,
		target: Callable[..., object] | None = None,
		event: Event = Event(),
		name: str | None = None,
		args: Iterable[Any] = (),
		kwargs: Mapping[str, Any] | None = None,
		*,
		daemon: bool | None = None
	) -> None:

		self.__target = target
		self.__args = args
		self.__kwargs = kwargs
		self.event = event

		super().__init__(
			group, target, name,
			args, kwargs, daemon = daemon
		)


	def run(self):
		try:
			if self.__target is not None:
				if not self.__kwargs:
					self.__target(self.event, *self.__args)
				else:
					self.__target(self.event, *self.__args, **self.__kwargs)
		finally:
			# Avoid a refcycle if the thread is running a function with
			# an argument that has a member that points to the thread.
			del self.__target, self.__args, self.__kwargs


	def wait(self, timeout: float | None = None) -> None:
		self.join(timeout)


	def stop(self):
		self.event.set()