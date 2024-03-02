# Inspired by https://gitlab.com/RemixDev/deemix-py/-/blob/main/deemix/utils/crypto.py?ref_type=heads

from requests import get as req_get

from ..exceptions.no_stream_data import No_Stream_Data

from .utils import (
	dec_chunk, gen_blowfish_key
)


__DEFAULT_BLOCK = 2048
__DEFAULT_BLOCK_STREAM = __DEFAULT_BLOCK * 3

# Thank you RemixDev without you this would be useless https://gitlab.com/RemixDev/deemix-py/-/blob/main/deemix/decryption.py?ref_type=heads#L84
# Also you https://gist.github.com/aleandroid/cbd675e1655e22b2727ef02dedfe3dfb#file-deez-revived-user-js-L1042

def decrypt_track(id_track: str, media_url: str, save_path: str):
	blowfish_key = gen_blowfish_key(id_track)

	# from what I understand every 6144 (2048 * 3) bytes the first 2048 bytes are encrypted using blowfish, this till the end. If a final chunck is lower than 2048 bytes is not encrypted

	with (
		req_get(media_url, stream = True) as resp,
	):
		if resp.status_code != 200:
			raise No_Stream_Data(id_track, save_path)

		with open(save_path, 'wb') as f:
			for chunk in resp.iter_content(__DEFAULT_BLOCK_STREAM):
				l_chunk = len(chunk)

				if l_chunk >= __DEFAULT_BLOCK:
					decrypted_chunk = dec_chunk(
						blowfish_key, chunk[:__DEFAULT_BLOCK]
					)

					f.write(decrypted_chunk)
					chunk = chunk[__DEFAULT_BLOCK:]

				f.write(chunk)