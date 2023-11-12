# https://stackoverflow.com/questions/34073370/best-way-to-receive-the-return-value-from-a-python-generator

from typing import cast

from ..types.aliases import (
	G_Playlist, G_DW_Track, G_DW_Playlist,
	DW_Track
)


#https://stackoverflow.com/questions/34073370/best-way-to-receive-the-return-value-from-a-python-generator


class Gen_Playlist:
	def __init__(self, gen: G_Playlist) -> None:
		self.__gen = gen
		self.__first()


	def __first(self) -> None:
		# https://adamj.eu/tech/2021/07/06/python-type-hints-how-to-use-typing-cast/#the-simplest-cast

		self.playlist = next(
			cast(G_DW_Playlist, self.__gen)
		)


	def dw(self) -> DW_Track:
		return next(
			cast(G_DW_Track, self.__gen)
		)


	def __iter__(self) -> G_DW_Track:
		yield from cast(G_DW_Track, self.__gen)


	def wait(self) -> None:
		for _ in self.__gen:
			...