# https://stackoverflow.com/questions/34073370/best-way-to-receive-the-return-value-from-a-python-generator

from ..types.aliases import (
	G_Playlist, G_DW_Track,
	DW_Playlist, DW_Track
)


class Gen_Playlist:
	def __init__(self, gen: G_Playlist) -> None:
		self.__gen = gen
		self.__first()


	def __first(self) -> None:
		self.playlist: DW_Playlist = next(self.__gen) #pyright: ignore [reportArgumentType]


	def dw(self) -> DW_Track:
		return next(self.__gen) #pyright: ignore [reportArgumentType]


	def __iter__(self) -> G_DW_Track:
		yield from self.__gen #pyright: ignore [reportReturnType]


	def wait(self) -> None:
		for _ in self.__gen:
			...