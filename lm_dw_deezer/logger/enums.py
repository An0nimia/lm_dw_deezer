from enum import IntEnum

from logging import (
	INFO, WARNING, ERROR,
	DEBUG
)


class Level(IntEnum):
	INFO = INFO
	WARNING = WARNING
	ERROR = ERROR
	DEBUG = DEBUG