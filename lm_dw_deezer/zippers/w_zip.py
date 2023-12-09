from typing import cast

from pathlib import Path

from zipfile import (
	ZipFile, ZIP_DEFLATED
)

from ..types.aliases import (
	ITracks_Out, DW_Tracks, DW_Track
)


def __make_archive(
	dw_tracks: DW_Tracks | ITracks_Out,
	zip_file: ZipFile,
	archive_name: str
) -> None:

	if type(dw_tracks[0]) is DW_Track:
		__4_DW_Track(
			dw_tracks = cast(DW_Tracks, dw_tracks),
			zip_file = zip_file,
			archive_name = archive_name
		)
	else:
		__4_ITrack_out(
			dw_tracks = cast(ITracks_Out, dw_tracks),
			zip_file = zip_file,
			archive_name = archive_name
		)


def __4_DW_Track(
	dw_tracks: DW_Tracks,
	zip_file: ZipFile,
	archive_name: str
) -> None:

	for dw_track in dw_tracks:
		if dw_track.dw_track is None:
			continue

		zip_file.write(
			filename = dw_track.dw_track.path,
			arcname = f'{archive_name}/{Path(dw_track.dw_track.path).name}'
		)


def __4_ITrack_out(
	dw_tracks: ITracks_Out,
	zip_file: ZipFile,
	archive_name: str
) -> None:

	for dw_track in dw_tracks:
		if dw_track is None:
			continue

		zip_file.write(
			filename = dw_track.path,
			arcname = f'{archive_name}/{Path(dw_track.path).name}'
		)


def zipper(
	dir_name: str,
	dw_tracks: ITracks_Out | DW_Tracks
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