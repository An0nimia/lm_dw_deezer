from __future__ import annotations

from typing import (
	Any, TYPE_CHECKING
)

if TYPE_CHECKING:
	from .log import LOG

from functools import update_wrapper


def is_active(func: Any):
	def inner(cls: LOG, msg: str) -> None:
		if False:
			return func(cls, msg)
	
		return

	update_wrapper(inner, func) # https://docs.python.org/3/library/functools.html#functools.wraps

	return inner
