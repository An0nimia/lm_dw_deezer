def get_disk_info() -> str:
	return (
		'''
			diskInfo {
				diskNumber
				trackNumber
			}
		'''
	)


def get_lyrics_info() -> str:
	return (
		'''
			lyrics {
				id
				synchronizedLines {
					lrcTimestamp
					line
					milliseconds
					duration
				}
				text
				copyright
				writers
			}
		'''
	)


def get_album_info() -> str:
	return (
		'''
			album {
				label
				producerLine
				copyright
				discsCount
				tracksCount
			}
		'''
	)


def get_track() -> str:
	return (
		f'''
			{get_lyrics_info()}
			bpm
			{get_album_info()}
		'''
	)


def get_track_x_album() -> str:
	return (
		f'''
			edges {{
				node {{
					{get_lyrics_info()}
					bpm
				}}
			}}
		'''
	)


def get_track_edges() -> str:
	return (
		f'''
			edges {{
				node {{
					{get_track()}
					{get_disk_info()}
					releaseDate
				}}
			}}
		'''
	)


def get_album(n_tracks: int) -> str:
	return (
		f'''
			label
			producerLine
			copyright
			discsCount
			tracksCount
			tracks(first: {n_tracks}) {{
				{
					get_track_x_album()
				}
			}}
		'''
	)


def get_playlist(n_tracks: int) -> str:
	return (
		f'''
			id
			title
			description
			isPrivate
			isCollaborative
			isCharts
			isBlindTestable
			isFromFavoriteTracks
			isEditorialized
			picture {{
				url: urls(pictureRequest: {{width: 1400, height: 1400}})
			}}
			estimatedTracksCount
			estimatedDuration
			creationDate
			lastModificationDate
			fansCount
			isFavorite
			tracks(first: {n_tracks}) {{
				{
					get_track_edges()
				}
			}}
		'''
	)