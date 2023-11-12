from typing import Any

from .types import (
	get_track, get_track_edges, get_album, get_playlist
)


def get_track_query(id_track: str) -> dict[str, Any]:
	params = {
		'operationName': 'get_track',
		'variables': {
			'id_track': id_track,
		},
		'query': (
			f'''
				query get_track($id_track: String!) {{
					track(trackId: $id_track) {{
						{
							get_track()
						}
					}}
				}}
			'''
		)
	}

	return params


def get_tracks_query(id_tracks: list[str]) -> dict[str, Any]:
	params = {
		'operationName': 'get_tracks',
		'variables': {
			'id_tracks': id_tracks,
		},
		'query': (
			f'''
				query get_tracks($id_tracks: [String!]) {{
					tracks(trackIds: $id_tracks) {{
						{
							get_track_edges()
						}
					}}
				}}
			'''
		)
	}

	return params


def get_album_query(id_album: str, n_tracks: int) -> dict[str, Any]:
	params = {
		'operationName': 'get_album',
		'variables': {
			'id_album': id_album,
		},
		'query': (
			f'''
				query get_album($id_album: String!) {{
					album(albumId: $id_album) {{
						{
							get_album(n_tracks)
						}
					}}
				}}
			'''
		)
	}

	return params


def get_playlist_query(id_playlist: str, n_tracks: int) -> dict[str, Any]:
	params = {
		'operationName': 'get_playlist',
		'variables': {
			'id_playlist': id_playlist,
		},
		'query': (
			f'''
				query get_playlist($id_playlist: String!) {{
					playlist(playlistId: $id_playlist) {{
						{
							get_playlist(n_tracks)
						}
					}}
				}}
			'''
		)
	}

	return params