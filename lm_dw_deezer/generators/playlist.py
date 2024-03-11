# https://stackoverflow.com/questions/34073370/best-way-to-receive-the-return-value-from-a-python-generator

from ..types import DW_Playlist

from ..dw_helpers.playlist import (
	G_Playlist, G_DW_Playlist, Helper_Playlist
)


class Gen_Playlist:
	def __init__(self, gen: G_Playlist) -> None:
		self.__gen = gen
		self.__first()


	def __first(self) -> None:
		self.playlist: DW_Playlist = next(self.__gen) #pyright: ignore [reportArgumentType]


	def next(self) -> Helper_Playlist:
		return next(self.__gen) #pyright: ignore [reportArgumentType]


	def __iter__(self) -> G_DW_Playlist:
		yield from self.__gen #pyright: ignore [reportReturnType]


	def wait(self) -> None:
		track: Helper_Playlist
		for track in self.__gen: #pyright: ignore [reportAssignmentType]
			track.dw()