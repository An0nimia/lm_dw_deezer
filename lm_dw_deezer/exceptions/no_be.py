from ..config.enums import DECRYPTOR


class No_BE(Exception):
	def __init__(
		self,
		kind: DECRYPTOR,
		msg: str = 'Sorry not found necessary dependencies for using \'{}\' backend'
	) -> None:

		super().__init__(
			msg.format(kind)
		)