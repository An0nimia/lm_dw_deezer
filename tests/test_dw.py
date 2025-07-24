from unittest import TestCase

from lm_dw_deezer import (
	DW, Gen_Track, Gen_Album, config
)


class GW_Test(TestCase):
	__ARL = 'cbd1d223c47a2229c9b6c44e139cce996b5785f9f9debd82b2fa8bfa6d8a7645ff2eb5562183ca891691ef03e14c38f3ef4e8a1663c86376db65f961c7b45e96084d7a30699a04096cd1ef9642b8bad890416f01136f4e0fdec401926bb9155e'
	__api = DW(__ARL)
	__conf = config.CONF(DECRYPTOR = config.enums.DECRYPTOR.C)


	def test_dw_track(self):
		res = Gen_Track(self.__api.dw_track('2825782592', conf = self.__conf))
		res.wait()

		assert res.track.dw_track is not None


	def test_dw_album(self):
		res = Gen_Album(self.__api.dw_album('43274571', conf = self.__conf))
		res.wait()

		assert res.album.dw_tracks is not None


	def test_dw_album2(self):
		res = Gen_Album(self.__api.dw_album('103248', conf = self.__conf))
		res.wait()

		assert res.album.dw_tracks is not None
