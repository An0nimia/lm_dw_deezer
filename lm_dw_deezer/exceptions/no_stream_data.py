class No_Stream_Data(Exception):
	def __init__(
		self,
		id_track: str,
		unborn_path: str,
		msg: str = 'There is no audio stream for \'{}\' at the moment'
	) -> None:

		self.unborn_path = unborn_path

		super().__init__(
			msg.format(id_track)
		)