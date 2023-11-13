from typing import Any

from api_deezer_full.gw.types.track import (
	Track, Base_Track, DEFAULT_DATE
)


from .config.data_utils import COMPRESSION


from .types.aliases import (
	ITracks_Out, DW_Tracks
)

from .types.pipe_ext import (
	Playlist_Tracks, Playlist_Track,
)

from .zippers import (
	zipper, gzipper, zstdipper
)


def __normalize(
	pipe_playlist_track_JSON: dict[str, Any],
	pipe_playlist_track: Playlist_Track,
	gw_playlist_track: Base_Track
) -> None:

	pipe_playlist_track_JSON['GENRE_ID'] = '0'
	pipe_playlist_track_JSON['DIGITAL_RELEASE_DATE'] = pipe_playlist_track.release_date
	pipe_playlist_track_JSON['PHYSICAL_RELEASE_DATE'] = DEFAULT_DATE
	pipe_playlist_track_JSON['STATUS'] = True if not gw_playlist_track.fallback else False
	pipe_playlist_track_JSON['DISK_NUMBER'] = pipe_playlist_track.disk_info.disk_number


	if gw_playlist_track.fallback:
		__normalize(pipe_playlist_track_JSON['fallback'], pipe_playlist_track, gw_playlist_track.fallback)


def merge_track_data(
	pipe_playlist_tracks: Playlist_Tracks,
	gw_playlist_tracks: list[Base_Track]
) -> list[Track]:
	
	tracks: list[Track] = []

	for pipe_playlist_track, gw_playlist_track in zip(pipe_playlist_tracks, gw_playlist_tracks):
		pipe_playlist_track_JSON = pipe_playlist_track.model_dump()
		gw_playlist_track_JSON = gw_playlist_track.model_dump()
		pipe_playlist_track_JSON.update(gw_playlist_track_JSON)

		__normalize(
			pipe_playlist_track_JSON, pipe_playlist_track, gw_playlist_track
		)

		tracks.append(
			Track.model_validate(pipe_playlist_track_JSON)
		)

	return tracks


def make_archive(
	type_arc: COMPRESSION,
	dir_name: str,
	dw_tracks: ITracks_Out | DW_Tracks
) -> str:

	match type_arc:
		case COMPRESSION.ZIP:
			func = zipper
		case COMPRESSION.GZIP:
			func = gzipper
		case COMPRESSION.ZSTD:
			func = zstdipper

	return func(dir_name, dw_tracks)