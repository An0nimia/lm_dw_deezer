from pydantic import (
	BaseModel, Field
)

from api_deezer_full.pipe.types import Lyrics


class Base_Album(BaseModel):
	label: str | None = None
	producer: str | None = None
	disks_count: int = Field(validation_alias = 'discsCount')
	tracks_count: int = Field(validation_alias = 'tracksCount')


class Base_Track(BaseModel):
	lyrics: Lyrics | None
	bpm: float | None