from typing import cast

from pathlib import Path

from tarfile import TarFile

from ..types.aliases import (
	ITracks_Out, DW_Tracks, DW_Track
)


def make_archive(
	dw_tracks: DW_Tracks | ITracks_Out,
	tar: TarFile,
	archive_name: str
) -> None:

	if type(dw_tracks[0]) is DW_Track:
		__4_DW_Track(
			dw_tracks = cast(DW_Tracks, dw_tracks),
			tar = tar,
			archive_name = archive_name
		)
	else:
		__4_ITrack_out(
			dw_tracks = cast(ITracks_Out, dw_tracks),
			tar = tar,
			archive_name = archive_name
		)


def __4_DW_Track(
	dw_tracks: DW_Tracks,
	tar: TarFile,
	archive_name: str
) -> None:

	for dw_track in dw_tracks:
		if dw_track.dw_track is None:
			continue

		tar.add(
			name = dw_track.dw_track.path,
			arcname = f'{archive_name}/{Path(dw_track.dw_track.path).name}',
			recursive = False
		)


def __4_ITrack_out(
	dw_tracks: ITracks_Out,
	tar: TarFile,
	archive_name: str
) -> None:

	for dw_track in dw_tracks:
		if dw_track is None:
			continue

		tar.add(
			name = dw_track.path,
			arcname = f'{archive_name}/{Path(dw_track.path).name}',
			recursive = False
		)