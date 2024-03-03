from pathlib import Path

#from subprocess import check_output

from tarfile import open as TAR

from zstandard import ZstdCompressor

from ..types import (
	DW_Album, DW_Playlist
)

from .utils import make_archive


def zstd_compress(
	dir_name: str,
	dw_tracks: DW_Album | DW_Playlist
) -> str:

	zstd_name = Path(dir_name).name
	path = f'{dir_name}/{zstd_name}.tar.zst'
	cctx = ZstdCompressor()

	# creating a TAR which the content is gonna stream to the ZSTD stream writer for compression data
	# the zstd stream write is gonna to write to the physical file
	# https://stackoverflow.com/questions/76681159/what-is-the-most-efficient-way-to-unpack-a-tar-zstd-download-in-python

	with (
		open(path, 'wb') as to_stream,
		cctx.stream_writer(to_stream) as stream,
		TAR(mode = 'w|', fileobj = stream) as tar
	):
		make_archive(
			dw_tracks = dw_tracks,
			tar = tar,
			archive_name = zstd_name
		)

	return path


# I know this function sucks, probably could be exploited to a RCE, somebody wants to do a pentest?
# Would be better to create a proper Class to integrate with TarFile as this https://pyzstd.readthedocs.io/en/latest/#with-tarfile
# ... But for some reasons my tar comes with 15 more mb, I do not why & I didn't got the time to figure out
# CURRENTLY NOT USING. CTRL + SHIFT + 7 for un-comment seletected code
# def old_zstd_compress(
# 	dir_name: str,
# 	dw_tracks: ITracks_Out | DW_Tracks
# ) -> str:

# 	zstd_name = Path(dir_name)
# 	path = f'{zstd_name.name}/{zstd_name.name}.tar.zst'
# 	t = type(dw_tracks[0])

# 	kind = 0

# 	if t is DW_Track:
# 		kind = 1

# 	paths: list[str] = ['tar', '-I zstd --fast', '-cf', path]

# 	for dw_track in dw_tracks:
# 		if kind == 1:
# 			dw_track = cast(DW_Track, dw_track).dw_track
# 		else:
# 			dw_track = cast(Track_Out, dw_track)

# 		if dw_track is None:
# 			continue

# 		c_path = Path(dw_track.path)
# 		paths.append(f'{c_path.parent.name}/{c_path.name}')


# 	check_output(
# 		args = paths,
# 		cwd = zstd_name.parent.name
# 	)

# 	return path