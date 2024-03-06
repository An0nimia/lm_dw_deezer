from __future__ import annotations

from os import makedirs

from json import (
	dump as js_dump,
	load as js_load
)

from dataclasses import (
	dataclass, field, asdict
)

from .image import Image

from .thread_func import Thread_Func

from .utils import create_media_json
from .utils_infos import DEFAULT_SETTINGS_PATH

from .enums import (
	QUALITY as E_QUALITY,
	DECRYPTOR as E_DECRYPTOR,
	COMPRESSION as E_COMPRESSION,
	FILE_FORMAT as E_FILE_FORMAT,
	FOLDER_FORMAT as E_FOLDER_FORMAT
)


# https://stackoverflow.com/questions/52063759/passing-default-list-argument-to-dataclasses
@dataclass
class CONF:
	OUTPUT_FOLDER: str = 'Songs/'

	FILE_FORMAT: E_FILE_FORMAT | str = E_FILE_FORMAT.TITLE_ARTISTS_ISRC_QUALITY

	FOLDER_FORMAT: E_FOLDER_FORMAT | str = E_FOLDER_FORMAT.ALBUM_ARTISTS

	LEGACY_DOWNLOAD_RECURSION: bool = True

	RE_DOWNLOAD: bool = False

	ARCHIVE: E_COMPRESSION | None = None

	TRACK_IMAGE: Image = field(default_factory = Image)

	THREAD_FUNC: Thread_Func | None = None

	DECRYPTOR: E_DECRYPTOR = E_DECRYPTOR.C

	_QUALITIES: list[E_QUALITY] = field(
		default_factory = lambda: [quality for quality in E_QUALITY]
	)


	@property
	def QUALITIES(self) -> list[E_QUALITY]:
		return self._QUALITIES


	@QUALITIES.setter
	def QUALITIES(self, qualities: list[E_QUALITY]) -> None:
		self._QUALITIES = qualities #pyright: ignore [reportConstantRedefinition]
		self.MEDIA_FORMATS = create_media_json(self._QUALITIES)


	def __post_init__(self):
		makedirs(self.OUTPUT_FOLDER, exist_ok = True)
		self.QUALITIES = self._QUALITIES


	def export(self, output: str = DEFAULT_SETTINGS_PATH):
		with open(output, 'w') as f:
			js_settings = asdict(self)
			del js_settings['THREAD_FUNC']

			js_dump(
				js_settings, f,
				indent = 4
			)

	@staticmethod
	def jmport(input: str = DEFAULT_SETTINGS_PATH) -> CONF:
		with open(input, 'r') as f:
			js_settings = js_load(f)


		conf = CONF(**js_settings)
		conf.TRACK_IMAGE = Image(**js_settings['TRACK_IMAGE']) #pyright: ignore [reportConstantRedefinition]

		return conf