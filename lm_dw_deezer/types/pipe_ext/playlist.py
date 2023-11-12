from typing import Annotated
from datetime import datetime

from pydantic import (
	BaseModel, BeforeValidator, Field
)

from api_deezer_full.pipe.types import Cover

from api_deezer_full.pipe.types import Disk_Info

from .track import Track


class Playlist_Track(Track):
	disk_info: Disk_Info = Field(validation_alias = 'diskInfo')
	release_date: datetime = Field(validation_alias = 'releaseDate')


type _Playlist_Track = Annotated[
	Playlist_Track, BeforeValidator(
		lambda data: data['node']
	)
]


type Playlist_Tracks = Annotated[
	list[_Playlist_Track], BeforeValidator(
		lambda data: data['edges']
	)
]


class Playlist(BaseModel):
	id: str
	title: str
	description: str | None
	is_private: bool = Field(validation_alias = 'isPrivate')
	is_collaborative: bool = Field(validation_alias = 'isCollaborative')
	is_charts: bool = Field(validation_alias = 'isCharts')
	is_blind_testable: bool = Field(validation_alias = 'isBlindTestable')
	is_from_favorite_tracks: bool = Field(validation_alias = 'isFromFavoriteTracks')
	is_editorialized: bool = Field(validation_alias = 'isEditorialized')
	picture: Cover | None
	estimated_tracks_count: int = Field(validation_alias = 'estimatedTracksCount')
	estimated_duration: int = Field(validation_alias = 'estimatedDuration')
	creation_date: datetime = Field(validation_alias = 'creationDate')
	last_modification_date: datetime = Field(validation_alias = 'lastModificationDate')
	fans_count: int = Field(validation_alias = 'fansCount')
	tracks: Playlist_Tracks