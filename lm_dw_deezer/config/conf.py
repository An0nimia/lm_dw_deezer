from os import makedirs

from dataclasses import (
	dataclass, field
)

from .image import Image
from .thread_func import Thread_Func
from .utils import create_media_json

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
	QUALITIES: list[E_QUALITY] = field(
		default_factory = lambda: [quality for quality in E_QUALITY]
	)

	OUTPUT_FOLDER: str = 'Songs/'

	FILE_FORMAT: E_FILE_FORMAT | str = E_FILE_FORMAT.TITLE_ARTISTS_ISRC_QUALITY

	FOLDER_FORMAT: E_FOLDER_FORMAT | str = E_FOLDER_FORMAT.ALBUM_ARTISTS

	LEGACY_DOWNLOAD_RECURSION: bool = True
	RE_DOWNLOAD: bool = False
	ARCHIVE: E_COMPRESSION | None = None

	TRACKS_IMAGE: Image = field(default_factory = Image)
	THREAD_FUNC: Thread_Func | None = None
	DECRYPTOR: E_DECRYPTOR = E_DECRYPTOR.C


	def __post_init__(self):
		makedirs(self.OUTPUT_FOLDER, exist_ok = True)

		self.MEDIA_FORMATS = create_media_json(self.QUALITIES)