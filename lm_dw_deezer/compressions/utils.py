from __future__ import annotations

from pathlib import Path

from tarfile import TarFile

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..types import DW_Tracks



def make_archive(
	dw_tracks: DW_Tracks,
	tar: TarFile,
	archive_name: str
) -> None:
	__4_DW_Track(
		dw_tracks = dw_tracks,
		tar = tar,
		archive_name = archive_name
	)


def __4_DW_Track(
	dw_tracks: DW_Tracks,
	tar: TarFile,
	archive_name: str
) -> None:

	for dw_track in dw_tracks:
		if not dw_track.dw_track:
			continue

		arc_name = Path(dw_track.dw_track.path).name

		tar.add(
			name = dw_track.dw_track.path,
			arcname = f'{archive_name}/{arc_name}',
			recursive = False
		)