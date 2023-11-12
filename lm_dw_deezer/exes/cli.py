from typing import (
	Annotated, Optional
)

from typer import (
	Typer, Argument, Option
)

from api_deezer_full.media.exceptions import Insufficient_Rights

from ..logger import LOG

from ..config import (
	CONF, Thread_Func
)

from ..config.data_utils import (
	QUALITS, COMPRESSION, BE_DW
)

from ..generators import (
	Gen_Track, Gen_Album, Gen_Playlist
)

from .utils import (
	init_check, task
)


app = Typer()
default_conf = CONF()
api_dw = init_check()
LOG.disable_output()


@app.command(name = 'set-arl', help = 'For setting deezer arl cookie')
def set_arl() -> None:
	init_check(override = True)


@app.command(name = 'trk', help = 'For downloading tracks')
def trk(
	link: Annotated[
		str, Argument(
			help = 'A deezer track link or ID'
		)
	],

	quality: Annotated[
		list[QUALITS], Option(
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

	be_dw: Annotated[
		BE_DW, Option(
			help = 'Backed for downloading'
		)
	] = BE_DW.C
):

	conf = CONF(
		QUALITIES = quality,
		OUTPUT_FOLDER = out_dir,
		RE_DOWNLOAD = re_download,
		BACKEND_DW = be_dw
	)

	try:
		Gen_Track(
			api_dw.dw_track(link, conf)
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
		list[QUALITS], Option(
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

	be_dw: Annotated[
		BE_DW, Option(
			help = 'Backed for downloading'
		)
	] = BE_DW.C
):
	conf = CONF(
		QUALITIES = quality,
		OUTPUT_FOLDER = out_dir,
		RE_DOWNLOAD = re_download,
		ARCHIVE = archive,
		BACKEND_DW = be_dw
	)

	if fast:
		conf.THREAD_FUNC = Thread_Func(
			func = task,
			WORKERS = workers
		)

	album = Gen_Album(api_dw.dw_album(link, conf))
	album.wait()


@app.command()
def ply(
	link: Annotated[
		str, Argument(
			help = 'A deezer album link or ID'
		)
	],

	quality: Annotated[
		list[QUALITS], Option(
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

	be_dw: Annotated[
		BE_DW, Option(
			help = 'Backed for downloading'
		)
	] = BE_DW.C
):
	conf = CONF(
		QUALITIES = quality,
		OUTPUT_FOLDER = out_dir,
		RE_DOWNLOAD = re_download,
		ARCHIVE = archive,
		BACKEND_DW = be_dw,
	)

	if fast:
		conf.THREAD_FUNC = Thread_Func(
			WORKERS = workers,
			func = task
		)

	playlist = Gen_Playlist(api_dw.dw_playlist(link, conf))
	playlist.wait()


def main():
	app()


if __name__ == '__main__':
	main()