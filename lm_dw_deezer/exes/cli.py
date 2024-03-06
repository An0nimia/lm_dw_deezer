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

from ..config.conf import DEFAULT_SETTINGS_PATH

from ..config import (
	CONF, Thread_Func,
	QUALITY, COMPRESSION,
	DECRYPTOR, FILE_FORMAT, FOLDER_FORMAT
)

from ..generators import (
	Gen_Track, Gen_Album, Gen_Playlist
)

from .utils import (
	init_check, task,
	write_arl, import_conf
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

	config_path: Annotated[
		str, Option(
			help = f'The path where conf file is stored. Default is: \'{DEFAULT_SETTINGS_PATH}\''
		)
	] = DEFAULT_SETTINGS_PATH,

	quality: Annotated[
		Optional[list[QUALITY]], Option(
			case_sensitive = False,
			help = 'Choose download quality (Can specify multiple if you prefer a quality order)',
		)
	] = None,

	out_dir: Annotated[
		Optional[str], Option(
			help = 'Choose output dir'
		)
	] = None,

	re_download: Annotated[
		Optional[bool], Option(
			help = 'If track exist re-download it'
		)
	] = None,

	legacy_dw_recursion: Annotated[
		Optional[bool], Option(
			help = 'Try downloading track using old method'
		)
	] = None,

	file_format: Annotated[
		Optional[FILE_FORMAT], Option(
			help = 'File format for customize output filename'
		)
	] = None,

	c_file_format: Annotated[
		Optional[str], Option(
			help = 'File format for customize output filename, see the available params in \'file_format\' option'
		)
	] = None,

	folder_format: Annotated[
		Optional[FOLDER_FORMAT], Option(
			help = 'Folder format for customize output folder name'
		)
	] = None,

	c_folder_format: Annotated[
		Optional[str], Option(
			help = 'Folder format for customize output folder name, see the available params in \'folder_format\' option'
		)
	] = None,

	be_dw: Annotated[
		Optional[DECRYPTOR], Option(
			help = 'Backed for downloading'
		)
	] = None
):

	if c_file_format:
		file_format = c_file_format #pyright: ignore [reportAssignmentType]

	if c_folder_format:
		folder_format = c_folder_format #pyright: ignore [reportAssignmentType]

	conf = import_conf(config_path)

	if quality:
		conf.QUALITIES = quality
	if out_dir:
		conf.OUTPUT_FOLDER = out_dir
	if re_download:
		conf.RE_DOWNLOAD = re_download
	if legacy_dw_recursion:
		conf.LEGACY_DOWNLOAD_RECURSION = legacy_dw_recursion
	if file_format:
		conf.FILE_FORMAT = file_format
	if folder_format:
		conf.FOLDER_FORMAT = folder_format
	if be_dw:
		conf.DECRYPTOR = be_dw

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

	config_path: Annotated[
		str, Option(
			help = f'The path where conf file is stored. Default is: \'{DEFAULT_SETTINGS_PATH}\''
		)
	] = DEFAULT_SETTINGS_PATH,

	quality: Annotated[
		Optional[list[QUALITY]], Option(
			case_sensitive = False,
			help = 'Choose download quality (Can specify multiple if you prefer a quality order)',
		)
	] = None,

	out_dir: Annotated[
		Optional[str], Option(
			help = 'Choose output dir'
		)
	] = default_conf.OUTPUT_FOLDER,

	re_download: Annotated[
		Optional[bool], Option(
			help = 'If track exist re-download it'
		)
	] = None,

	legacy_dw_recursion: Annotated[
		Optional[bool], Option(
			help = 'Try downloading track using old method'
		)
	] = None,

	file_format: Annotated[
		Optional[FILE_FORMAT], Option(
			help = 'File format for customize output filename'
		)
	] = None,

	c_file_format: Annotated[
		Optional[str], Option(
			help = 'File format for customize output filename, see the available params in \'file_format\' option'
		)
	] = None,

	folder_format: Annotated[
		Optional[FOLDER_FORMAT], Option(
			help = 'Folder format for customize output folder name'
		)
	] = None,

	c_folder_format: Annotated[
		Optional[str], Option(
			help = 'Folder format for customize output folder name, see the available params in \'folder_format\' option'
		)
	] = None,

	be_dw: Annotated[
		Optional[DECRYPTOR], Option(
			help = 'Backed for downloading'
		)
	] = None,

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
	] = None
):
	if c_file_format:
		file_format = c_file_format #pyright: ignore [reportAssignmentType]

	if c_folder_format:
		folder_format = c_folder_format #pyright: ignore [reportAssignmentType]

	conf = import_conf(config_path)

	if quality:
		conf.QUALITIES = quality
	if out_dir:
		conf.OUTPUT_FOLDER = out_dir
	if re_download:
		conf.RE_DOWNLOAD = re_download
	if legacy_dw_recursion:
		conf.LEGACY_DOWNLOAD_RECURSION = legacy_dw_recursion
	if file_format:
		conf.FILE_FORMAT = file_format
	if folder_format:
		conf.FOLDER_FORMAT = folder_format
	if be_dw:
		conf.DECRYPTOR = be_dw
	if archive:
		conf.ARCHIVE = archive

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

	config_path: Annotated[
		str, Option(
			help = f'The path where conf file is stored. Default is: \'{DEFAULT_SETTINGS_PATH}\''
		)
	] = DEFAULT_SETTINGS_PATH,

	quality: Annotated[
		Optional[list[QUALITY]], Option(
			case_sensitive = False,
			help = 'Choose download quality (Can specify multiple if you prefer a quality order)',
		)
	] = None,

	out_dir: Annotated[
		Optional[str], Option(
			help = 'Choose output dir'
		)
	] = default_conf.OUTPUT_FOLDER,

	re_download: Annotated[
		Optional[bool], Option(
			help = 'If track exist re-download it'
		)
	] = None,

	legacy_dw_recursion: Annotated[
		Optional[bool], Option(
			help = 'Try downloading track using old method'
		)
	] = None,

	file_format: Annotated[
		Optional[FILE_FORMAT], Option(
			help = 'File format for customize output filename'
		)
	] = None,

	c_file_format: Annotated[
		Optional[str], Option(
			help = 'File format for customize output filename, see the available params in \'file_format\' option'
		)
	] = None,

	folder_format: Annotated[
		Optional[FOLDER_FORMAT], Option(
			help = 'Folder format for customize output folder name'
		)
	] = None,

	c_folder_format: Annotated[
		Optional[str], Option(
			help = 'Folder format for customize output folder name, see the available params in \'folder_format\' option'
		)
	] = None,

	be_dw: Annotated[
		Optional[DECRYPTOR], Option(
			help = 'Backed for downloading'
		)
	] = None,

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
	] = None
):	
	if c_file_format:
		file_format = c_file_format #pyright: ignore [reportAssignmentType]

	if c_folder_format:
		folder_format = c_folder_format #pyright: ignore [reportAssignmentType]

	conf = import_conf(config_path)

	if quality:
		conf.QUALITIES = quality
	if out_dir:
		conf.OUTPUT_FOLDER = out_dir
	if re_download:
		conf.RE_DOWNLOAD = re_download
	if legacy_dw_recursion:
		conf.LEGACY_DOWNLOAD_RECURSION = legacy_dw_recursion
	if file_format:
		conf.FILE_FORMAT = file_format
	if folder_format:
		conf.FOLDER_FORMAT = folder_format
	if be_dw:
		conf.DECRYPTOR = be_dw
	if archive:
		conf.ARCHIVE = archive

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