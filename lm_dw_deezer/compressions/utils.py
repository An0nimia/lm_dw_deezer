from pathlib import Path

from tarfile import TarFile

from ..types import (
	DW_Tracks, ITracks_Out,
	DW_Album, DW_Playlist
)


def make_archive(
	dw_tracks: DW_Album | DW_Playlist,
	tar: TarFile,
	archive_name: str
) -> None:
	if type(dw_tracks) is DW_Album:
		__4_ITrack_out(
			dw_tracks = dw_tracks.dw_tracks,
			tar = tar,
			archive_name = archive_name
		)
	elif type(dw_tracks) is DW_Playlist:
		__4_DW_Track(
			dw_tracks = dw_tracks.dw_tracks,
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

		arc_name = Path(dw_track.dw_track.path).name

		tar.add(
			name = dw_track.dw_track.path,
			arcname = f'{archive_name}/{arc_name}',
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

		arc_name = Path(dw_track.path).name

		tar.add(
			name = dw_track.path,
			arcname = f'{archive_name}/{arc_name}',
			recursive = False
		)