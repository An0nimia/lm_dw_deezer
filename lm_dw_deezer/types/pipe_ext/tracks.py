from typing import Annotated

from pydantic import (
	BaseModel, BeforeValidator, Field
)

from .track import Track


type _Track = Annotated[
	Track, BeforeValidator(
		lambda data: data['node']
	)
]


class Tracks(BaseModel):
	tracks: list[_Track] = Field(validation_alias = 'edges')