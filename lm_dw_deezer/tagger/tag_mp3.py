#pyright: reportUnknownMemberType=false

from __future__ import annotations

from typing import Any

from datetime import date

from mutagen.id3._specs import PictureType

from mutagen.id3 import ID3

from mutagen.id3._frames import (
	APIC, COMM, RVA2, TBPM,
	SYLT, USLT, TALB, TENC,
	TSRC, TPE1, TCOM, TPRO,
	TIT2, TCOP, TRCK, TPOS,
	TLEN, TEXT, TPUB, TDOR,
	TIPL, TDRL, TDRC
)

from api_deezer_full.pipe.types import Synchronized_Line

from api_deezer_full.gw.types import (
	Contributors, Artists
)

from .helpers import (
	lyric_w_time, get_contributors, get_composers
)

from .utils_infos import (
	SOURCE, ENCODER
)

# https://gitlab.com/RemixDev/deemix-py/-/blob/main/deemix/tagger.py?ref_type=heads
# https://mutagen-specs.readthedocs.io/en/latest/id3/id3v2.4.0-frames.html
# https://web.archive.org/web/20150620064121/http://id3.org/id3v2.4.0-frames


class TAG_MP3:
	def __init__(self, file_path: str) -> None:
		self.__file_path = file_path

	
	def __enter__(self) -> TAG_MP3:
		self.__tagger = ID3()

		return self


	def __exit__(self, exc_type: Any, exc_value: Any, exc_tb: Any) -> None:
		self.__tagger.save(self.__file_path)


	def add_image(self, image_bytes: bytes) -> None:
		self.__tagger.add(
			APIC(
				type = PictureType.COVER_FRONT,
				data = image_bytes
			)
		)


	def add_comment(self) -> None:
		self.__tagger.add(
			COMM(
				text = SOURCE
			)
		)


	def add_gain(self, gain: float) -> None:
		self.__tagger.add(
			RVA2(
				gain = gain
			)
		)


	def add_lyric_sync(self, synchronized_lines: list[Synchronized_Line]) -> None:
		self.__tagger.add( # poweramp android app for viewing synced lyric
			USLT(
				text = lyric_w_time(synchronized_lines)
			)
		)


	def add_lyric_sync_new(self, synchronized_lines: list[Synchronized_Line]) -> None:
		# https://web.archive.org/web/20200702111417/https://id3.org/id3v2.3.0#sec4.10
		
		infos_sync = [
			(
				info_sync.line, info_sync.milliseconds
			)
			for info_sync in synchronized_lines
		]

		self.__tagger.add( # poweramp android app for viewing synced lyric
			SYLT(
				type = 1,
				format = 2,
				text = infos_sync
			)
		)


	def add_album_name(self, album_name: str) -> None:
		self.__tagger.add(
			TALB(
				text = album_name
			)
		)


	def add_bpm(self, bpm: float) -> None:
		self.__tagger.add(
			TBPM(
				text = str(bpm)
			)
		)


	def add_contributors(self, contributors: Contributors) -> None:
		self.__tagger.add(
			TIPL(
				people = get_contributors(contributors)
			)
		)


	def add_composers(self, contributors: Contributors) -> None:
		self.__tagger.add(
			TCOM(
				text = get_composers(contributors)
			)
		)


	def add_copyright(self, copyright: str) -> None:
		self.__tagger.add(
			TCOP(
				text = copyright
			)
		)


	def add_date_original_release(self, date: date) -> None:
		self.__tagger.add(
			TDOR(
				text = f'{date.year}-{date.month:02d}-{date.day:02d}' # https://web.archive.org/web/20150619192102/http://id3.org/id3v2.4.0-structure
			)
		)


	def add_date_release(self, date: date) -> None:
		self.__tagger.add(
			TDRL(
				text = f'{date.year}-{date.month:02d}-{date.day:02d}'
			)
		)

		# MP3 players read this field for knowing the year of the track, even if for the specs it is the recording time

		self.__tagger.add(
			TDRC(
				text = f'{date.year}-{date.month:02d}-{date.day:02d}'
			)
		)


	def add_encoder(self) -> None:
		self.__tagger.add(
			TENC(
				text = ENCODER
			)
		)


	def add_lyricist(self, writers: list[str]) -> None:
		self.__tagger.add(
			TEXT(
				text = writers
			)
		)


	def add_title(self, title: str) -> None:
		self.__tagger.add(
			TIT2(
				text = title
			)
		)


	def add_audio_length(self, duration: int) -> None:
		self.__tagger.add(
			TLEN(
				text = str(duration * 1000)
			)
		)


	def add_isrc(self, isrc: str) -> None:
		self.__tagger.add(
			TSRC(
				text = isrc
			)
		)


	def add_artists(self, artists: Artists) -> None:
		self.__tagger.add(
			TPE1(
				text = [artist.name for artist in artists]
			)
		)


	def add_producer(self, label: str) -> None:
		self.__tagger.add(
			TPRO(
				text = label
			)
		)


	def add_publisher(self, producer_line: str) -> None:
		self.__tagger.add(
			TPUB(
				text = producer_line
			)
		)


	def add_track_number(self, track_number: int) -> None:
		self.__tagger.add(
			TRCK(
				text = f'{track_number}'
			)
		)


	def add_disk_number(self, disk_number: int, disks_count: int) -> None:
		self.__tagger.add(
			TPOS(
				text = f'{disk_number}/{disks_count}'
			)
		)


	def add_lyric_unsync(self, text: str) -> None:
		self.__tagger.add(
			USLT(
				text = text
			)
		)