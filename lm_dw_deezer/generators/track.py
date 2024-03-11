# https://stackoverflow.com/questions/34073370/best-way-to-receive-the-return-value-from-a-python-generator

from ..types import DW_Track


from ..dw_helpers.track import (
	G_Track, G_DW_Track, Helper_Track
)


class Gen_Track:
	def __init__(self, gen: G_Track) -> None:
		self.__gen = gen
		self.__first()


	def __first(self) -> None:
		self.track: DW_Track = next(self.__gen) #pyright: ignore [reportArgumentType]


	def next(self) -> Helper_Track:
		return next(self.__gen) #pyright: ignore [reportArgumentType]


	def __iter__(self) -> G_DW_Track:
		yield from self.__gen #pyright: ignore [reportReturnType]


	def wait(self) -> None:
		track: Helper_Track
		for track in self.__gen: #pyright: ignore [reportAssignmentType]
			track.dw()