from os import makedirs

from dataclasses import (
	dataclass, field
)

from .image import Image
from .thread_func import Thread_Func
from .utils import create_media_json

from .data_utils import (
	DEFAULT_FILE_FORMATS, QUALITS,
	DEFAULT_FOLDER_FORMATS, COMPRESSION, BE_DW
)


@dataclass
class CONF:
	QUALITIES: list[QUALITS] = field(
		default_factory = lambda: [
			QUALITS.NICE, QUALITS.GOOD, QUALITS.OK
		]
	) # https://stackoverflow.com/questions/52063759/passing-default-list-argument-to-dataclasses

	OUTPUT_FOLDER: str = 'Songs/'

	FILE_FORMATS: list[str] = field(default_factory = lambda: DEFAULT_FILE_FORMATS)
	FILE_FORMAT: int = -1

	FOLDER_FORMATS: list[str] = field(default_factory = lambda: DEFAULT_FOLDER_FORMATS)
	FOLDER_FORMAT: int = 0

	LEGACY_DOWNLOAD_RECURSION: bool = True
	RE_DOWNLOAD: bool = False
	ARCHIVE: COMPRESSION | None = None

	TRACKS_IMAGE: Image = field(default_factory = Image)
	THREAD_FUNC: Thread_Func | None = None
	BACKEND_DW: BE_DW = BE_DW.C


	def __post_init__(self):
		makedirs(self.OUTPUT_FOLDER, exist_ok = True)

		self.MEDIA_FORMATS = create_media_json(self.QUALITIES)

		self.FILE_TEMPLATE = self.FILE_FORMATS[self.FILE_FORMAT]

		self.FOLDER_TEMPLATE = self.FOLDER_FORMATS[self.FOLDER_FORMAT]