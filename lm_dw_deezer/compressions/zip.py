from pathlib import Path

from zipfile import (
	ZipFile, ZIP_DEFLATED
)

from ..types.dw_track import DW_Tracks


def __make_archive(
	dw_tracks: DW_Tracks,
	zip_file: ZipFile,
	archive_name: str
) -> None:
	__4_DW_Track(
		dw_tracks = dw_tracks,
		zip_file = zip_file,
		archive_name = archive_name
	)


def __4_DW_Track(
	dw_tracks: DW_Tracks,
	zip_file: ZipFile,
	archive_name: str
) -> None:

	for dw_track in dw_tracks:
		if not dw_track.dw_track:
			continue

		arc_name = f'{Path(dw_track.dw_track.path).name}'

		zip_file.write(
			filename = dw_track.dw_track.path,
			arcname = f'{archive_name}/{arc_name}'
		)


def zip_compress(
	dir_name: str,
	dw_tracks: DW_Tracks
) -> str:

	zip_name = Path(dir_name).name
	path = f'{dir_name}/{zip_name}.zip'

	with ZipFile(
		path, 'w',
		compression = ZIP_DEFLATED,
		compresslevel = 6 # Should be the most efficent https://docs.python.org/3/library/zlib.html#zlib.compressobj
	) as zip_file:
		__make_archive(
			dw_tracks = dw_tracks,
			zip_file = zip_file,
			archive_name = zip_name
		)

	return path