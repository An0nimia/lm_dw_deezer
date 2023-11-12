# https://stackoverflow.com/questions/34073370/best-way-to-receive-the-return-value-from-a-python-generator

from typing import cast

from ..types.aliases import (
	G_Track, G_Track_Out,
	G_DW_Track, ITrack_Out
)


class Gen_Track:
	def __init__(self, gen: G_Track) -> None:
		self.__gen = gen
		self.__first()


	def __first(self) -> None:
		# https://adamj.eu/tech/2021/07/06/python-type-hints-how-to-use-typing-cast/#the-simplest-cast

		self.track = next(
			cast(G_DW_Track, self.__gen)
		)


	def dw(self) -> ITrack_Out:
		return next(
			cast(G_Track_Out, self.__gen)
		)


	def __iter__(self) -> G_Track_Out:
		yield from cast(G_Track_Out, self.__gen)


	def wait(self) -> None:
		for _ in self.__gen:
			...