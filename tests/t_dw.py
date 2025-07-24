from threading import Event

from lm_dw_deezer import (
	DW, Gen_T_Track
)

from lm_dw_deezer.dw_helpers import Helper_Album, Helper_Playlist, Helper_T_Tracks
from lm_dw_deezer.config import CONF, Thread_Func

import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level = logging.DEBUG)

def task(event: Event, media: Helper_Album | Helper_Playlist | Helper_T_Tracks):
	media.dw()

__ARL = 'cbd1d223c47a2229c9b6c44e139cce996b5785f9f9debd82b2fa8bfa6d8a7645ff2eb5562183ca891691ef03e14c38f3ef4e8a1663c86376db65f961c7b45e96084d7a30699a04096cd1ef9642b8bad890416f01136f4e0fdec401926bb9155e'
__api = DW(__ARL)
conf = CONF()
conf.THREAD_FUNC = Thread_Func(
	func = task,
	WORKERS = 4
)
res = Gen_T_Track(
	__api.dw_T_tracks(['2825782592', '1529801692'], conf)
)

res.wait()
