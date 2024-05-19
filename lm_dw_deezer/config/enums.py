from __future__ import annotations

from enum import StrEnum


class QUALITY(StrEnum):
	NICE = 'MP3_320'
	GOOD = 'FLAC'
	OK = 'MP3_128'


	@classmethod
	def get_quality(cls, quality: str) -> QUALITY:
		return QUALITIES[quality]


QUALITIES = {
	quality.value: quality
	for quality in QUALITY
}


class COMPRESSION(StrEnum):
	ZSTD = 'ZSTD'
	ZIP = 'ZIP'
	GZIP = 'GZIP'


class DECRYPTOR(StrEnum):
	C = 'C'
	RUST = 'RUST'


class FILE_FORMAT(StrEnum):
	TITLE_ARTIST_ISRC = '{title} - {artist} ({ISRC})'
	TITLE_ARTIST = '{title} - {artist}'
	TITLE_ARTIST_QUALITY = '{title} - {artist} ({QUALITY})'
	ARTIST_TITLE = '{artist} - {title}'
	ALBUM_ARTIST_TITLE_QUALITY = '{album} - {artist} - {title} ({QUALITY})'
	TITLE_ARTISTS_QUALITY = '{title} - {artists} ({QUALITY})'
	ALBUM_TITLE = '{album} {title}'
	ALBUM_N_TRACK_N_DISK = '{album} {n_track}:{n_disk}'
	TITLE_ARTISTS_ISRC_QUALITY = '{title} - {artists} {ISRC} ({QUALITY})'


class FOLDER_FORMAT(StrEnum):
	ALBUM_ARTISTS = '{album} - {artists}'
	ARTIST_ALBUM = '{artist} - {album}'