
from api_deezer_full.gw.types import Track as GW_Track

from ..logger import LOG

from ..types import Track_Out

from ..types.pipe_ext import (
	Base_Track as PIPE_Track,
	Base_Album as PIPE_Album
)

from .tag_mp3 import TAG_MP3
from .tag_flac import TAG_FLAC
from .helpers import generate_rgain
from .utils import DEFAULT_PHYSICAL_RELEASE_DATE

def tagger_track(
	gw_info: GW_Track,
	out: Track_Out | None,
	pipe_info: PIPE_Track,
	pipe_info_album: PIPE_Album | None,
	image_bytes: bytes,
) -> None:

	if not out is None and not pipe_info_album is None:
		LOG.info(f'Adding tag to \'{gw_info.title}\'')

		tag(
			gw_track_info = gw_info,
			pipe_track_info = pipe_info,
			pipe_album_info = pipe_info_album,
			path = out.path,
			image_bytes = image_bytes,
			type_media = out.media_format
		)

		LOG.info(f'Successful downloaded \'{gw_info.title}\' at \'{out.path}\'')
	else:
		LOG.warning(f'Track \'{gw_info.title}\' - \'{gw_info.artists[0].name}\' cannot be downloaded')


def tag(
	gw_track_info: GW_Track,
	pipe_track_info: PIPE_Track,
	pipe_album_info: PIPE_Album,
	path: str,
	image_bytes: bytes,
	type_media: str
) -> None:

	tagger = TAG_MP3

	if type_media == 'flac':
		tagger = TAG_FLAC

	with tagger(path) as tagger:
		tagger.add_image(image_bytes)
		tagger.add_comment()

		if gw_track_info.gain:
			tagger.add_gain(
				generate_rgain(gw_track_info.gain)
			)

		if type_media != 'flac':
			tagger.add_audio_length(-gw_track_info.duration)

		lyrics = pipe_track_info.lyrics

		if lyrics:
			if lyrics.writers:
				tagger.add_lyricist(lyrics.writers.split(', '))

			if lyrics.copyright:
				tagger.add_copyright(lyrics.copyright)

			if lyrics.synchronized_lines:
				tagger.add_lyric_sync(lyrics.synchronized_lines)
			else:
				tagger.add_lyric_unsync(lyrics.text)

		tagger.add_album_name(gw_track_info.album_title)

		if pipe_track_info.bpm:
			tagger.add_bpm(pipe_track_info.bpm)

		tagger.add_contributors(gw_track_info.contributors)
		tagger.add_composers(gw_track_info.contributors)

		if gw_track_info.physical_release_date != DEFAULT_PHYSICAL_RELEASE_DATE: # Track from playlist doesn't have this JSON in their field
			tagger.add_date_original_release(gw_track_info.physical_release_date)

		tagger.add_date_release(gw_track_info.digital_release_date)
		tagger.add_encoder()
		tagger.add_title(gw_track_info.title)
		tagger.add_isrc(gw_track_info.ISRC)

		tagger.add_artists(gw_track_info.artists)

		if pipe_album_info.label:
			tagger.add_producer(pipe_album_info.label)

		if pipe_album_info.producer:
			tagger.add_publisher(pipe_album_info.producer)

		tagger.add_track_number(gw_track_info.track_number)
		tagger.add_disk_number(gw_track_info.disk_number, pipe_album_info.disks_count)