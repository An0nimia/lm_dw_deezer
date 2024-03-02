# https://stackoverflow.com/questions/34073370/best-way-to-receive-the-return-value-from-a-python-generator

from ..types.aliases import (
	G_Album, G_Track_Out, 
	ITrack_Out, DW_Album
)


class Gen_Album:
	def __init__(self, gen: G_Album) -> None:
		self.__gen = gen
		self.__first()


	def __first(self) -> None:
		self.album: DW_Album = next(self.__gen) #pyright: ignore [reportArgumentType]


	def dw(self) -> ITrack_Out:
		return next(self.__gen) #pyright: ignore [reportReturnType]


	def __iter__(self) -> G_Track_Out:
		yield from self.__gen #pyright: ignore [reportReturnType]


	def wait(self) -> None:
		for _ in self.__gen:
			...