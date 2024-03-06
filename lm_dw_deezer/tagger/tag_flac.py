#pyright: reportUnknownMemberType=false, reportOptionalSubscript=false, reportIndexIssue=false

from __future__ import annotations

from typing import Any

from datetime import date

from mutagen.flac import (
	FLAC, Picture
)

from mutagen.id3._specs import PictureType

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
# https://www.xiph.org/vorbis/doc/v-comment.html#fieldnames


class TAG_FLAC:
	def __init__(self, file_path: str) -> None:
		self.__file_path = file_path


	def __enter__(self) -> TAG_FLAC:
		self.__tagger = FLAC(self.__file_path)

		return self


	def __exit__(self, exc_type: Any, exc_value: Any, exc_tb: Any) -> None:
		self.__tagger.save()


	def add_image(self, image_bytes: bytes) -> None:
		pic = Picture()
		pic.type = PictureType.COVER_FRONT
		pic.data = image_bytes

		self.__tagger.add_picture(
			picture = pic
		)


	def add_comment(self) -> None:
		self.__tagger.tags['comment'] = SOURCE


	def add_gain(self, gain: float) -> None:
		self.__tagger.tags['REPLAYGAIN_TRACK_GAIN'] = str(gain)


	def add_lyric_sync(self, synchronized_lines: list[Synchronized_Line]) -> None:
		self.__tagger.tags['lyrics'] = lyric_w_time(synchronized_lines)


	def add_album_name(self, album_name: str) -> None:
		self.__tagger.tags['album'] = album_name


	def add_bpm(self, bpm: float) -> None:
		self.__tagger.tags['bpm'] = str(bpm)


	def add_contributors(self, contributors: Contributors) -> None:
		end = ''

		for role, name in get_contributors(contributors):
			end += f'{role}/{name}/'

		self.__tagger.tags['performer'] = end[:1]


	def add_composers(self, contributors: Contributors) -> None:
		self.__tagger.tags['composer'] = get_composers(contributors)


	def add_copyright(self, copyright: str) -> None:
		self.__tagger.tags['copyright'] = copyright


	def add_date_original_release(self, date: date) -> None:
		self.__tagger['physical_date'] = f'{date.year}-{date.month:02d}-{date.day:02d}'


	def add_date_release(self, date: date) -> None:
		self.__tagger['date'] = f'{date.year}-{date.month:02d}-{date.day:02d}'


	def add_encoder(self) -> None:
		self.__tagger.tags['encodedby'] = ENCODER


	def add_lyricist(self, writers: list[str]) -> None:
		self.__tagger.tags['lyricist'] = writers


	def add_title(self, title: str) -> None:
		self.__tagger.tags['title'] = title


	def add_audio_length(self, duration: int) -> None:
		...


	def add_isrc(self, isrc: str) -> None:
		self.__tagger.tags['isrc'] = isrc


	def add_artists(self, artists: Artists) -> None:
		self.__tagger.tags['artist'] = [artist.name for artist in artists]


	def add_producer(self, label: str) -> None:
		self.__tagger.tags['ORGANIZATION'] = label


	def add_publisher(self, producer_line: str) -> None:
		self.__tagger.tags['license'] = producer_line


	def add_track_number(self, track_number: int) -> None:
		self.__tagger.tags['tracknumber'] = str(track_number)


	def add_disk_number(self, disk_number: int, disks_count: int) -> None:
		self.__tagger.tags['discnumber'] = str(disk_number)
		self.__tagger.tags['totaldiscs'] = str(disks_count)


	def add_lyric_unsync(self, text: str) -> None:
		self.__tagger.tags['lyrics'] = text