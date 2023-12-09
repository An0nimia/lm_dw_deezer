from enum import StrEnum


class QUALITS(StrEnum):
	NICE = 'MP3_320'
	GOOD = 'FLAC'
	OK = 'MP3_128'


class COMPRESSION(StrEnum):
	ZSTD = 'ZSTD'
	ZIP = 'ZIP'
	GZIP = 'GZIP'


class BE_DW(StrEnum):
	C = 'C'
	RUST = 'RUST'


DEFAULT_FILE_FORMATS = [
	'{title} - {artist} ({ISRC})',
	'{title} - {artist}',
	'{title} - {artist} ({QUALITY})',
	'{artist} - {title}',
	'{album} - {artist} - {title} ({QUALITY})',
	'{title} - {artists} ({QUALITY})',
	'{album} {title}',
	'{album} {n_track}:{n_disk}',
	'{title} - {artists} {ISRC} ({QUALITY})'
]


DEFAULT_FOLDER_FORMATS = [
	'{album} - {artists}',
	'{artist} - {album}'
]