from pathlib import Path

from tarfile import open as TAR

from ..types import (
	DW_Album, DW_Playlist
)

from .utils import make_archive


def gzip_compress(
	dir_name: str,
	dw_tracks: DW_Album | DW_Playlist
) -> str:

	gz_name = Path(dir_name).name
	path = f'{dir_name}/{gz_name}.tar.gz'

	with TAR(path, 'w:gz') as tar:
		make_archive(
			dw_tracks = dw_tracks,
			tar = tar,
			archive_name = gz_name
		)

	return path
