#pyright: reportUnusedImport=false

from threading import Event

from collections.abc import (
	Callable, Iterator
)

from .track_out import ITrack_Out

from .dw_track import DW_Track
from .dw_album import DW_Album
from .dw_playlist import DW_Playlist

type G_Track_Out = Iterator[ITrack_Out]

type G_DW_Track = Iterator[DW_Track]
type G_DW_Album = Iterator[DW_Album]
type G_DW_Playlist = Iterator[DW_Playlist]

type G_Track = Iterator[DW_Track | ITrack_Out]
type G_Album = Iterator[DW_Album | ITrack_Out]
type G_Playlist = Iterator[DW_Playlist | DW_Track]

type F_THREAD = Callable[
	[Event, G_DW_Track | G_Track_Out], None
] | None

type F_BE_DW = Callable[
	[str, str, str], None
]