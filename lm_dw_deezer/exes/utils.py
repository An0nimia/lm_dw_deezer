from typer import prompt

from os.path import isfile

from threading import Event

from api_deezer_full.gw.exceptions import Arl_Invalid

from ..config import CONF

from ..dw_helpers import (
	Helper_Album, Helper_Playlist
)



from json import (
	load as JSON_load,
	dumps as JSON_dumps
)

from .data_utils import (
	l_browsers, file_conf
)

from .read_browsers_cookies import (
	read_firefox, #read_chrome
)

from ..dw import DW


def write_arl(arl: str):
	infos = {
		'arl': arl
	}

	JSON_conf = JSON_dumps(infos, indent = 4)

	with open(file_conf, 'w') as fn:
		fn.write(JSON_conf)


def __get_arl():
	with open(file_conf) as f:
		data = JSON_load(f)
		arl = data['arl']	

	return arl


def check_arl(override: bool = False) -> str:
	if not override and isfile(file_conf):
		return __get_arl()

	choice = l_browsers.execute()

	match choice:
		case 'firefox':
			arl = read_firefox()
		# case 'chrome':
		# 	arl = read_chrome()
		case _:
			arl = prompt('Please input your arl')

	if not arl:
		arl = prompt('Please input your arl')

	write_arl(arl)

	return arl


def init_check(override: bool = False) -> DW:
	while True:
		try:
			api_dw = DW(check_arl(override))
			return api_dw
		except Arl_Invalid as err:
			print(err.message)
			override = True
		except KeyboardInterrupt:
			exit()


def task(event: Event, media: Helper_Album | Helper_Playlist):
	media.dw()


def import_conf(conf_path: str) -> CONF:
	conf = CONF()

	if isfile(conf_path):
		conf = CONF.jmport(conf_path)

	return conf