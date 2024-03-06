from Cryptodome.Hash import MD5

from Cryptodome.Cipher import (
	AES, Blowfish
)

# https://gitlab.com/RemixDev/deemix-py/-/blob/main/deemix/utils/crypto.py?ref_type=heads

from .utils_infos import (
	FMTS_CODES, SECRET_KEY, IV,
	OLD_URL_MEDIA_TEMPLATE, SECRET
)


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
			md5, FMTS_CODES[quality], id_track, media_version
		]
	)

	hashed = MD5.new(data).hexdigest().encode()

	data = b'\xa4'.join(
		[hashed, data]
	) + b'\xa4'

	if len(data) % 16:
		data += b'\x00' * (16 - len(data) % 16)

	c = AES.new(SECRET_KEY, AES.MODE_ECB) #pyright: ignore [reportUnknownMemberType]

	media = c.encrypt(data).hex()

	return OLD_URL_MEDIA_TEMPLATE.format(
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
			ord(SECRET[i])
		)

	return bf_key.encode()


def dec_chunk(blowfish_key: bytes, data: bytes) -> bytes:
	blow = Blowfish.new( #pyright: ignore [reportUnknownMemberType]
		key = blowfish_key,
		mode = Blowfish.MODE_CBC,
		iv = IV
	)

	return blow.decrypt(data)