from logging import (
	StreamHandler, Formatter, FileHandler,
	getLogger
)

from .enums import Level


class LOG:
	__LOGGER = 'DW_DEEZER'
	__F_LOGGER = 'lm_dw_deezer.log'
	__FORMATER = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


	@classmethod
	def __init__(cls) -> None:
		cls.__logger = getLogger(cls.__LOGGER)
		cls.progress_bar = True
		cls.enable_output()


	@classmethod
	def enable_output(cls) -> None:
		cls.set_stream_handler()


	@classmethod
	def disable_output(cls) -> None:
		cls.__logger.removeHandler(cls.__s_handler)


	@classmethod
	def set_file_handler(cls, level: Level = Level.WARNING) -> None:
		cls.__f_handler = FileHandler(cls.__F_LOGGER)
		cls.__f_handler.setFormatter(cls.__FORMATER)
		cls.__f_handler.setLevel(level)
		cls.__logger.addHandler(cls.__f_handler)
		cls.__logger.setLevel(level)


	@classmethod
	def set_stream_handler(cls, level: Level = Level.INFO) -> None:
		cls.__s_handler = StreamHandler()
		cls.__s_handler.setLevel(level)
		cls.__s_handler.setFormatter(cls.__FORMATER)
		cls.__logger.addHandler(cls.__s_handler)
		cls.__logger.setLevel(level)


	@classmethod
	def set_stream_debug_handler(cls) -> None:
		cls.disable_output()
		cls.set_stream_handler(Level.DEBUG)


	@classmethod
	def set_file_debug_handler(cls) -> None:
		cls.set_file_handler(Level.DEBUG)


	@classmethod
	def warning(cls, msg: str) -> None:
		cls.__logger.warning(msg)


	@classmethod
	def error(cls, msg: str) -> None:
		cls.__logger.error(msg)


	@classmethod
	def debug(cls, msg: str) -> None:
		cls.__logger.debug(msg)


	@classmethod
	def info(cls, msg: str) -> None:
		cls.__logger.info(msg)