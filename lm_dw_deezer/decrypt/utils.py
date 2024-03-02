from Cryptodome.Hash import MD5

from Cryptodome.Cipher import (
	AES, Blowfish
)

# https://gitlab.com/RemixDev/deemix-py/-/blob/main/deemix/utils/crypto.py?ref_type=heads

__SECRET = 'g4el58wc0zvf9na1'
__IV = b'\x00\x01\x02\x03\x04\x05\x06\x07'
__SECRET_KEY = b'jo6aey6haid2Teih'
__URL_MEDIA_TEMPLATE = 'https://e-cdns-proxy-{md5_0}.dzcdn.net/mobile/1/{media}'

__FMTS_CODES = {
	'MP3_128': '1',
	'MP3_320': '3', # they are just here for legacy reason, only MP3_128 is gonna work
	'FLAC': '9'
}

def __md5(data: str) -> str:
	h = MD5.new()

	h.update(
		data.encode() 
	)

	return h.hexdigest()


def gen_song_hash(
	md5: str,
	quality: str,
	id_track: str,
	media_version: str
) -> str:

	data = b'\xa4'.join(
		a.encode()
		for a in [
			md5, __FMTS_CODES[quality], id_track, media_version
		]
	)

	hashed = MD5.new(data).hexdigest().encode()

	data = b'\xa4'.join(
		[hashed, data]
	) + b'\xa4'

	if len(data) % 16:
		data += b'\x00' * (16 - len(data) % 16)

	c = AES.new(__SECRET_KEY, AES.MODE_ECB) # pyright: ignore

	media = c.encrypt(data).hex()

	return __URL_MEDIA_TEMPLATE.format(
		md5_0 = md5[0],
		media = media
	)


def gen_blowfish_key(id_track: str) -> bytes:
	id_md5 = __md5(id_track)

	bf_key = ''

	for i in range(16):
		bf_key += chr(
			ord(id_md5[i]) ^
			ord(id_md5[i + 16]) ^
			ord(__SECRET[i])
		)

	return bf_key.encode()


def dec_chunk(blowfish_key: bytes, data: bytes) -> bytes:
	blow = Blowfish.new( # pyright: ignore
		key = blowfish_key,
		mode = Blowfish.MODE_CBC,
		iv = __IV
	)

	return blow.decrypt(data)