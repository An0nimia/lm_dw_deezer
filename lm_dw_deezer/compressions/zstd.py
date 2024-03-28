from pathlib import Path

from tarfile import open as TAR

from zstandard import ZstdCompressor

from ..types.dw_track import DW_Tracks

from .utils import make_archive


def zstd_compress(
	dir_name: str,
	dw_tracks: DW_Tracks
) -> str:

	zstd_name = Path(dir_name).name
	path = f'{dir_name}/{zstd_name}.tar.zst'
	cctx = ZstdCompressor()

	# creating a TAR which the content is gonna stream to the ZSTD stream writer for compression data
	# the zstd stream write is gonna to write to the physical file
	# https://stackoverflow.com/questions/76681159/what-is-the-most-efficient-way-to-unpack-a-tar-zstd-download-in-python

	with (
		open(path, 'wb') as to_stream,
		cctx.stream_writer(to_stream) as stream,
		TAR(mode = 'w|', fileobj = stream) as tar
	):
		make_archive(
			dw_tracks = dw_tracks,
			tar = tar,
			archive_name = zstd_name
		)

	return path