from ..config.data_utils import BE_DW


class No_BE(Exception):
	def __init__(
		self,
		kind: BE_DW,
		msg: str = 'Sorry not found necessary dependencies for using \'{}\' backend'
	) -> None:

		super().__init__(
			msg.format(kind)
		)