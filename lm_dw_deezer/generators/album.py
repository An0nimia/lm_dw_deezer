# https://stackoverflow.com/questions/34073370/best-way-to-receive-the-return-value-from-a-python-generator


from ..types import DW_Album

from ..dw_helpers.album import (
	G_Album, G_DW_Album, Helper_Album
)


class Gen_Album:
	def __init__(self, gen: G_Album) -> None:
		self.__gen = gen
		self.__first()


	def __first(self) -> None:
		self.album: DW_Album = next(self.__gen) #pyright: ignore [reportArgumentType]


	def next(self) -> Helper_Album:
		return next(self.__gen) #pyright: ignore [reportArgumentType]


	def __iter__(self) -> G_DW_Album:
		yield from self.__gen #pyright: ignore [reportReturnType]


	def wait(self) -> None:
		album: Helper_Album
		for album in self.__gen: #pyright: ignore [reportAssignmentType]
			album.dw()