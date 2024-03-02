from sys import argv

from typing import (
	Annotated, Optional
)

from typer import (
	Typer, Argument, Option
)

from api_deezer_full import API_Mobile
from api_deezer_full.media.exceptions import Insufficient_Rights

from ..logger import LOG

from ..config import (
	CONF, Thread_Func
)

from ..config.enums import (
	QUALITY, COMPRESSION,
	DECRYPTOR, FILE_FORMAT, FOLDER_FORMAT
)

from ..generators import (
	Gen_Track, Gen_Album, Gen_Playlist
)

from .utils import (
	init_check, task, write_arl
)


app = Typer()
default_conf = CONF()

if len(argv) != 1 and not argv[1] in ('set-arl', 'login'):
	api_dw = init_check()

LOG.disable_output()


@app.command(name = 'set-arl', help = 'For setting deezer arl cookie')
def set_arl() -> None:
	init_check(override = True)
	print('ARL is set')


@app.command(name = 'login', help = 'For setting deezer arl cookie with username & password')
def login(
	email: Annotated[
		str, Option(
			prompt = True
		)
	],
	password: Annotated[
		str, Option(
			prompt = True,
			hide_input = True
		)
	]
) -> None:

	api_mobile = API_Mobile(email, password)
	api_mobile.login()
	write_arl(api_mobile.ARL)
	print('Logged successfully =)')


@app.command(name = 'trk', help = 'For downloading tracks')
def trk(
	link: Annotated[
		str, Argument(
			help = 'A deezer track link or ID'
		)
	],

	quality: Annotated[
		list[QUALITY], Option(
			case_sensitive = False,
			help = 'Choose download quality (Can specify multiple if you prefer a quality order)',
		)
	] = default_conf.QUALITIES,

	out_dir: Annotated[
		str, Option(
			help = 'Choose output dir'
		)
	] = default_conf.OUTPUT_FOLDER,

	re_download: Annotated[
		bool, Option(
			help = 'If track exist re-download it'
		)
	] = default_conf.RE_DOWNLOAD,

	file_format: Annotated[
		FILE_FORMAT, Option(
			help = 'File format for customize output filename'
		)
	] = FILE_FORMAT.TITLE_ARTISTS_ISRC_QUALITY,

	c_file_format: Annotated[
		Optional[str], Option(
			help = 'File format for customize output filename, see the available params in \'file_format\' option'
		)
	] = None,

	folder_format: Annotated[
		FOLDER_FORMAT, Option(
			help = 'Folder format for customize output folder name'
		)
	] = FOLDER_FORMAT.ALBUM_ARTISTS,

	c_folder_format: Annotated[
		Optional[str], Option(
			help = 'Folder format for customize output folder name, see the available params in \'folder_format\' option'
		)
	] = None,

	be_dw: Annotated[
		DECRYPTOR, Option(
			help = 'Backed for downloading'
		)
	] = DECRYPTOR.C
):

	if not c_file_format is None:
		file_format = c_file_format #pyright: ignore [reportAssignmentType]

	if not c_folder_format is None:
		folder_format = c_folder_format #pyright: ignore [reportAssignmentType]

	conf = CONF(
		QUALITIES = quality,
		OUTPUT_FOLDER = out_dir,
		RE_DOWNLOAD = re_download,
		DECRYPTOR = be_dw,
		FILE_FORMAT = file_format,
		FOLDER_FORMAT = folder_format
	)

	try:
		Gen_Track(
			api_dw.dw_track(link, conf) #pyright: ignore [reportPossiblyUnboundVariable]
		).wait()
	except Insufficient_Rights as err:
		print(err.message)



@app.command()
def alb(
	link: Annotated[
		str, Argument(
			help = 'A deezer album link or ID'
		)
	],

	quality: Annotated[
		list[QUALITY], Option(
			help = 'Choose download quality (Can specify multiple if you prefer a quality order)',
		)
	] = default_conf.QUALITIES,

	out_dir: Annotated[
		str, Option(
			help = 'Choose output dir'
		)
	] = default_conf.OUTPUT_FOLDER,

	re_download: Annotated[
		bool, Option(
			help = 'If track exist re-download it'
		)
	] = default_conf.RE_DOWNLOAD,

	fast: Annotated[
		bool, Option(
			'--fast/--slow',
			help = 'Do you want to see some real speed?'
		)
	] = False,

	workers: Annotated[
		int,  Option(
			help = 'Number of parallel threads for downloading'
		)
	] = 3,

	archive: Annotated[
		Optional[COMPRESSION], Option(
			help = 'Archive type'
		)
	] = None,

	file_format: Annotated[
		FILE_FORMAT, Option(
			help = 'File format for customize output filename'
		)
	] = FILE_FORMAT.TITLE_ARTISTS_ISRC_QUALITY,

	c_file_format: Annotated[
		Optional[str], Option(
			help = 'File format for customize output filename, see the available params in \'file_format\' option'
		)
	] = None,

	folder_format: Annotated[
		FOLDER_FORMAT, Option(
			help = 'Folder format for customize output folder name'
		)
	] = FOLDER_FORMAT.ALBUM_ARTISTS,

	c_folder_format: Annotated[
		Optional[str], Option(
			help = 'Folder format for customize output folder name, see the available params in \'folder_format\' option'
		)
	] = None,

	be_dw: Annotated[
		DECRYPTOR, Option(
			help = 'Backed for downloading'
		)
	] = DECRYPTOR.C
):
	if not c_file_format is None:
		file_format = c_file_format #pyright: ignore [reportAssignmentType]

	if not c_folder_format is None:
		folder_format = c_folder_format #pyright: ignore [reportAssignmentType]

	conf = CONF(
		QUALITIES = quality,
		OUTPUT_FOLDER = out_dir,
		RE_DOWNLOAD = re_download,
		ARCHIVE = archive,
		DECRYPTOR = be_dw,
		FILE_FORMAT = file_format,
		FOLDER_FORMAT = folder_format
	)

	if fast:
		conf.THREAD_FUNC = Thread_Func(
			func = task,
			WORKERS = workers
		)

	album = Gen_Album(api_dw.dw_album(link, conf)) #pyright: ignore [reportPossiblyUnboundVariable]
	album.wait()


@app.command()
def ply(
	link: Annotated[
		str, Argument(
			help = 'A deezer album link or ID'
		)
	],

	quality: Annotated[
		list[QUALITY], Option(
			help = 'Choose download quality (Can specify multiple if you prefer a quality order)',
		)
	] = default_conf.QUALITIES,

	out_dir: Annotated[
		str, Option(
			help = 'Choose output dir'
		)
	] = default_conf.OUTPUT_FOLDER,

	re_download: Annotated[
		bool, Option(
			help = 'If track exist re-download it'
		)
	] = default_conf.RE_DOWNLOAD,

	fast: Annotated[
		bool, Option(
			'--fast/--slow',
			help = 'Do you want to see some real speed?'
		)
	] = False,

	workers: Annotated[
		int,  Option(
			help = 'Number of parallel threads for downloading'
		)
	] = 3,

	archive: Annotated[
		Optional[COMPRESSION], Option(
			help = 'Archive type'
		)
	] = None,

	file_format: Annotated[
		FILE_FORMAT, Option(
			help = 'File format for customize output filename'
		)
	] = FILE_FORMAT.TITLE_ARTISTS_ISRC_QUALITY,

	c_file_format: Annotated[
		Optional[str], Option(
			help = 'File format for customize output filename, see the available params in \'file_format\' option'
		)
	] = None,

	folder_format: Annotated[
		FOLDER_FORMAT, Option(
			help = 'Folder format for customize output folder name'
		)
	] = FOLDER_FORMAT.ALBUM_ARTISTS,

	c_folder_format: Annotated[
		Optional[str], Option(
			help = 'Folder format for customize output folder name, see the available params in \'folder_format\' option'
		)
	] = None,

	be_dw: Annotated[
		DECRYPTOR, Option(
			help = 'Backed for downloading'
		)
	] = DECRYPTOR.C
):	
	if not c_file_format is None:
		file_format = c_file_format #pyright: ignore [reportAssignmentType]

	if not c_folder_format is None:
		folder_format = c_folder_format #pyright: ignore [reportAssignmentType]

	conf = CONF(
		QUALITIES = quality,
		OUTPUT_FOLDER = out_dir,
		RE_DOWNLOAD = re_download,
		ARCHIVE = archive,
		DECRYPTOR = be_dw,
		FILE_FORMAT = file_format,
		FOLDER_FORMAT = folder_format
	)

	if fast:
		conf.THREAD_FUNC = Thread_Func(
			WORKERS = workers,
			func = task
		)

	playlist = Gen_Playlist(api_dw.dw_playlist(link, conf)) #pyright: ignore [reportPossiblyUnboundVariable]
	playlist.wait()


def main():
	app()


if __name__ == '__main__':
	main()