
from api_deezer_full.gw.types.track import DEFAULT_DATE

from ..logger import LOG

from ..types.pipe_ext import Base_Album as PIPE_Base_Album

from ..types import (
	Track_Out, DW_Track
)

from .tag_mp3 import TAG_MP3
from .tag_flac import TAG_FLAC
from .helpers import generate_rgain


def tagger_track(
	pipe_info_album: PIPE_Base_Album | None,
	dw_track: DW_Track,
	image_bytes: bytes
) -> None:

	if dw_track.dw_track and pipe_info_album:
		LOG.info(f'Adding tag to \'{dw_track.gw_info.title}\'')

		tag(
			dw_track = dw_track,
			pipe_album_info = pipe_info_album,
			image_bytes = image_bytes,
		)

		LOG.info(f'Successful downloaded \'{dw_track.gw_info.title}\' at \'{dw_track.dw_track.path}\'')
	else:
		LOG.warning(f'Track \'{dw_track.gw_info.title}\' - \'{dw_track.gw_info.artists[0].name}\' cannot be downloaded')


def tag(
	dw_track: DW_Track,
	pipe_album_info: PIPE_Base_Album,
	image_bytes: bytes
) -> None:

	tagger = TAG_MP3
	track_out: Track_Out = dw_track.dw_track #pyright: ignore [reportAssignmentType]

	if track_out.quality == 'FLAC':
		tagger = TAG_FLAC

	with tagger(track_out.path) as tagger:
		tagger.add_image(image_bytes)
		tagger.add_comment()

		if dw_track.gw_info.gain:
			tagger.add_gain(
				generate_rgain(dw_track.gw_info.gain)
			)

		if track_out.quality == 'FLAC':
			tagger.add_audio_length(dw_track.gw_info.duration)

		lyrics = dw_track.pipe_info.lyrics

		if lyrics:
			if lyrics.writers:
				tagger.add_lyricist(lyrics.writers.split(', '))

			if lyrics.copyright:
				tagger.add_copyright(lyrics.copyright)

			if lyrics.synchronized_lines:
				tagger.add_lyric_sync(lyrics.synchronized_lines)
			else:
				tagger.add_lyric_unsync(lyrics.text)

		tagger.add_album_name(dw_track.gw_info.album_title)

		if dw_track.pipe_info.bpm:
			tagger.add_bpm(dw_track.pipe_info.bpm)

		tagger.add_contributors(dw_track.gw_info.contributors)
		tagger.add_composers(dw_track.gw_info.contributors)

		if dw_track.gw_info.physical_release_date != DEFAULT_DATE: # Track from playlist doesn't have this JSON in their field
			tagger.add_date_original_release(dw_track.gw_info.physical_release_date)

		if dw_track.gw_info.digital_release_date != DEFAULT_DATE:
			tagger.add_date_release(dw_track.gw_info.digital_release_date)

		tagger.add_encoder()
		tagger.add_title(dw_track.gw_info.title)
		tagger.add_isrc(dw_track.gw_info.ISRC)

		tagger.add_artists(dw_track.gw_info.artists)

		if pipe_album_info.label:
			tagger.add_producer(pipe_album_info.label)

		if pipe_album_info.producer:
			tagger.add_publisher(pipe_album_info.producer)

		tagger.add_track_number(dw_track.gw_info.track_number)
		tagger.add_disk_number(dw_track.gw_info.disk_number, pipe_album_info.disks_count)