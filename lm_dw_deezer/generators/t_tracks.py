# https://stackoverflow.com/questions/34073370/best-way-to-receive-the-return-value-from-a-python-generator

from ..types import DW_T_Tracks


from ..dw_helpers.t_tracks import (
	G_T_Tracks, G_DW_T_Tracks, Helper_T_Tracks
)


class Gen_T_Track:
	def __init__(self, gen: G_T_Tracks) -> None:
		self.__gen = gen
		self.__first()


	def __first(self) -> None:
		self.t_tracks: DW_T_Tracks = next(self.__gen) #pyright: ignore [reportAttributeAccessIssue]


	def next(self) -> Helper_T_Tracks:
		return next(self.__gen) #pyright: ignore [reportReturnType]


	def __iter__(self) -> G_DW_T_Tracks:
		yield from self.__gen #pyright: ignore [reportReturnType]


	def wait(self) -> None:
		track: Helper_T_Tracks
		for track in self.__gen: #pyright: ignore [reportAssignmentType]
			track.dw()
