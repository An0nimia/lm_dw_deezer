from ..medjays import DW_Medjay
from ..config.enums import COMPRESSION

from ..compressions import (
	zip_compress, gzip_compress, zstd_compress
)

from .dw_track import DW_Tracks


def wait_threads(threads: list[DW_Medjay]) -> None:
	for thread in threads:
		thread.wait()

	threads.clear()


def make_archive(
	type_arc: COMPRESSION,
	dir_name: str,
	dw_tracks: DW_Tracks
) -> str:

	match type_arc:
		case COMPRESSION.ZIP:
			func = zip_compress
		case COMPRESSION.GZIP:
			func = gzip_compress
		case COMPRESSION.ZSTD:
			func = zstd_compress

	return func(dir_name, dw_tracks)