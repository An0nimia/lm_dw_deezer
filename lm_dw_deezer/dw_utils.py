from tqdm import tqdm

from api_deezer_full.media.types import Medias

from importlib.util import find_spec

be_dw_rust_supported = find_spec('lm_deezer_bf_dec')

if not be_dw_rust_supported is None:
	from lm_deezer_bf_dec import decrypt_track as decrypt_track_w_RUST
else:
	decrypt_track_w_RUST = None

from api_deezer_full.gw.types import Track
from api_deezer_full.media.types import Medias

from .logger import LOG
from .exceptions import No_BE
from .decrypt import decrypt_track as decrypt_track_w_C

from .medjays import (
	DW_Medjay, Event
)

from .config.enums import DECRYPTOR

from .config import (
	CONF, Thread_Func
)

from .types.aliases import (
	G_Track_Out, G_DW_Track, F_BE_DW
)

from .types import (
	DW_Album, DW_Playlist
)

from .types.pipe_ext import (
	Playlist as PIPE_Playlist
)

from .dw_helpers import (
	helper_album, helper_playlist
)


def get_pbar(medias: Medias, tracks: list[Track]):
	p_bar = tqdm(
		zip(
			medias.medias, tracks
		),
		disable = not LOG.progress_bar,
		desc = 'Starting downloading...',
		total = len(tracks),
		ascii = "▯▮"
	)

	return p_bar


def wait_threads(threads: list[DW_Medjay]) -> None:
	for thread in threads:
		thread.wait()

	threads.clear()


def get_be_dw(backend_dw: DECRYPTOR) -> F_BE_DW:
	match backend_dw:
		case DECRYPTOR.RUST:
			if decrypt_track_w_RUST is None:
				raise No_BE(DECRYPTOR.RUST)

			be_dw = decrypt_track_w_RUST
		case DECRYPTOR.C:
			be_dw = decrypt_track_w_C

	return be_dw


def dw_album_seq(
	medias: Medias,
	album_info: DW_Album,
	conf: CONF,
	dir_name: str
) -> G_Track_Out:

	p_bar = get_pbar(medias, album_info.gw_tracks_info)
	dw_helper = get_be_dw(conf.DECRYPTOR)

	for (media, gw_track_info), pipe_track_info in zip(
		p_bar, album_info.pipe_info.tracks
	):
		p_bar.set_description(f'Downloading {gw_track_info.title}')

		yield from helper_album(
			gw_track_info = gw_track_info,
			media = media,
			conf = conf,
			pipe_track_info = pipe_track_info,
			dir_name = dir_name,
			album_info = album_info,
			func_be_dw = dw_helper
		)


def dw_album_thread(
	medias: Medias,
	album_info: DW_Album,
	conf: CONF,
	dir_name: str,
) -> None:

	thread_func: Thread_Func = conf.THREAD_FUNC #pyright: ignore [reportAssignmentType]
	threads: list[DW_Medjay] = []
	event = Event()
	workers = thread_func.WORKERS
	p_bar = get_pbar(medias, album_info.gw_tracks_info)
	dw_helper = get_be_dw(conf.DECRYPTOR)

	for (media, gw_track_info), pipe_track_info in zip(
		p_bar, album_info.pipe_info.tracks
	):
		p_bar.set_description(f'Downloading {gw_track_info.title}')

		helper = helper_album(
			gw_track_info = gw_track_info,
			media = media,
			conf = conf,
			pipe_track_info = pipe_track_info,
			dir_name = dir_name,
			album_info = album_info,
			func_be_dw = dw_helper
		)

		if workers == 0:
			wait_threads(threads)

			if event.is_set():
				break

			workers = thread_func.WORKERS

		c_thread = DW_Medjay(
			target = thread_func.func,
			args = (helper,),
			event = event
		)

		c_thread.start()
		threads.append(c_thread)
		workers -= 1

	wait_threads(threads)


def dw_playlist_seq(
	medias: Medias,
	playlist_info: DW_Playlist,
	pipe_info: PIPE_Playlist,
	tracks: list[Track],
	conf: CONF,
	dir_name: str
) -> G_DW_Track:

	p_bar = get_pbar(medias, tracks)
	dw_helper = get_be_dw(conf.DECRYPTOR)

	for (media, gw_track_info), pipe_track_info in zip(
		p_bar, pipe_info.tracks
	):
		p_bar.set_description(f'Downloading {gw_track_info.title}')

		yield from helper_playlist(
			gw_track_info = gw_track_info,
			media = media,
			conf = conf,
			pipe_track_info = pipe_track_info,
			dw_tracks = playlist_info.dw_tracks,
			dir_name = dir_name,
			func_be_dw = dw_helper
		)


def dw_playlist_thread(
	medias: Medias,
	playlist_info: DW_Playlist,
	pipe_info: PIPE_Playlist,
	tracks: list[Track],
	conf: CONF,
	dir_name: str
) -> None:

	thread_func: Thread_Func = conf.THREAD_FUNC #pyright: ignore [reportAssignmentType]
	threads: list[DW_Medjay] = []
	workers = thread_func.WORKERS
	event = Event()
	p_bar = get_pbar(medias, tracks)
	dw_helper = get_be_dw(conf.DECRYPTOR)

	for (media, gw_track_info), pipe_track_info in zip(
		p_bar, pipe_info.tracks
	):
		p_bar.set_description(f'Downloading {gw_track_info.title}')

		helper = helper_playlist(
			gw_track_info = gw_track_info,
			media = media,
			conf = conf,
			pipe_track_info = pipe_track_info,
			dw_tracks = playlist_info.dw_tracks,
			dir_name = dir_name,
			func_be_dw = dw_helper
		)

		if workers == 0:
			wait_threads(threads)

			if event.is_set():
				break

			workers = thread_func.WORKERS

		c_thread = DW_Medjay(
			target = thread_func.func,
			args = (helper,),
			event = event
		)

		c_thread.start()
		threads.append(c_thread)
		workers -= 1

	wait_threads(threads)