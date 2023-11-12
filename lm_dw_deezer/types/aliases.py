# pyright: reportUnusedImport=false

from threading import Event

from collections.abc import (
	Generator, Callable
)

from .dw_track import (
	DW_Track, Track_Out, ITrack_Out
)

from .dw_album import (
	DW_Album, ITracks_Out
)

from .dw_playlist import (
	DW_Playlist, DW_Tracks
)


type G_DW_Track = Generator[DW_Track, None, None]
type G_DW_Album = Generator[DW_Album, None, None]
type G_DW_Playlist = Generator[DW_Playlist, None, None]

type G_Track_Out = Generator[ITrack_Out, None, None]

type G_Track = Generator[
	DW_Track | ITrack_Out, None, None
]

type G_Album = Generator[
	DW_Album | ITrack_Out, None, None
]

type G_Playlist = Generator[
	DW_Playlist | DW_Track, None, None
]

type F_THREAD = Callable[
	[Event, G_DW_Track | G_Track_Out], None
] | None

type F_BE_DW = Callable[
	[str, str, str], None
]