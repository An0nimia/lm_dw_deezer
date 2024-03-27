from api_deezer_full import (
	API_PIPE, API_Media
)

from .logger import LOG
from .config import CONF

from .dw_helpers.utils import (
	create_dir, create_dir_w_track
)

from .utils import merge_track_data

from .dw_utils import (
	dw_track_seq, dw_album_seq, dw_album_thread,
	dw_playlist_seq, dw_playlist_thread
)

from .graphql.queries import (
	get_track_query, get_album_query, get_playlist_query
)

from .generators import (
	G_Track, G_Album, G_Playlist
)


from .types import (
	DW_Track, DW_Album, DW_Playlist
)

from .types.pipe_ext import (
	Track as PIPE_Track,
	Album as PIPE_Album,
	Playlist as PIPE_Playlist
)


LOG()

class DW(API_PIPE):
	def __init__(self, arl: str) -> None:
		super().__init__(arl) # init the father I mean the API instance


	def dw_track(
		self,
		link: str,
		conf: CONF = CONF()
	) -> G_Track:

		LOG.info(f'Getting infos on \'{link}\'')
		gw_info = self.gw_get_track(link)
		LOG.debug(gw_info.__str__())
		LOG.info(f'GOT infos on \'{link}\'')
		LOG.info(f'Looking out for sources for \'{gw_info.title}\'')

		pipe_JSON = self.pipe_make_req(
			get_track_query(gw_info.id)
		)['data']['track']

		pipe_info = PIPE_Track.model_validate(pipe_JSON)

		dw_track = DW_Track(
			image = conf.TRACK_IMAGE,
			gw_info = gw_info,
			pipe_info = pipe_info
		)

		yield dw_track

		track_token = gw_info.track_token

		if gw_info.fallback:
			track_token = gw_info.fallback.track_token

		media_infos = API_Media.get_medias(
			license_token = self.license_token,
			media_formats = [conf.MEDIA_FORMATS],
			track_tokens = [track_token]
		)

		dir_name = create_dir_w_track(conf, gw_info)

		yield from dw_track_seq(
			medias = media_infos,
			dw_track = dw_track,
			conf = conf,
			dir_name = dir_name
		)


	def dw_album(
		self,
		link: str,
		conf: CONF = CONF()
	) -> G_Album:

		LOG.info(f'Getting infos on \'{link}\'')
		gw_info = self.gw_get_album(link)
		album_info = gw_info.tracks[0]
		LOG.info(f'GOT infos on \'{link}\'')
		LOG.info(f'Looking out for tracks sources in \'{album_info.album_title}\'')

		pipe_JSON = self.pipe_make_req(
			get_album_query(album_info.id_album, gw_info.total)
		)['data']['album']

		pipe_info = PIPE_Album.model_validate(pipe_JSON)

		album_info = DW_Album(
			image = conf.TRACK_IMAGE,
			gw_tracks_info = gw_info.tracks,
			pipe_info = pipe_info,
			dir_name = create_dir_w_track(conf, gw_info.tracks[0])
		)

		yield album_info

		tracks_token: list[str] = []

		for track in gw_info.tracks:
			track_token = track.track_token

			if track.fallback:
				track_token = track.fallback.track_token

			tracks_token.append(track_token)

		medias = API_Media.get_medias(
			license_token = self.license_token,
			media_formats = [conf.MEDIA_FORMATS] * pipe_info.tracks_count,
			track_tokens = tracks_token
		)

		LOG.info('GOT track sources')

		if not conf.THREAD_FUNC:
			yield from dw_album_seq(
				medias = medias,
				album_info = album_info,
				conf = conf
			)
		else:
			dw_album_thread(
				medias = medias,
				album_info = album_info,
				conf = conf
			)

		if conf.ARCHIVE:
			album_info.create_archive(conf.ARCHIVE)


	def dw_playlist(
		self,
		link: str,
		conf: CONF = CONF()
	) -> G_Playlist:

		LOG.info(f'Getting infos on \'{link}\'')
		playlist_data = self.gw_get_playlist(link)
		LOG.info(f'GOT infos on \'{link}\'')

		pipe_JSON = self.pipe_make_req(
			get_playlist_query(playlist_data.id, playlist_data.total)
		)['data']['playlist']

		pipe_info = PIPE_Playlist.model_validate(pipe_JSON)

		playlist_info = DW_Playlist(
			pipe_info = pipe_info,
			gw_tracks_info = merge_track_data(pipe_info.tracks, playlist_data.tracks),
			dir_name = create_dir(conf, pipe_info.title)
		)

		yield playlist_info

		tracks_token: list[str] = []

		for track_data in playlist_data.tracks:
			track_token = track_data.track_token

			if track_data.fallback:
				track_token = track_data.fallback.track_token

			tracks_token.append(track_token)

		medias = API_Media.get_medias(
			license_token = self.license_token,
			media_formats = [conf.MEDIA_FORMATS] * pipe_info.estimated_tracks_count,
			track_tokens = tracks_token
		)

		if not conf.THREAD_FUNC:
			yield from dw_playlist_seq(
				medias = medias,
				playlist_info = playlist_info,
				conf = conf
			)
		else:
			dw_playlist_thread(
				medias = medias,
				playlist_info = playlist_info,
				conf = conf
			)

		if conf.ARCHIVE:
			playlist_info.create_archive(conf.ARCHIVE)