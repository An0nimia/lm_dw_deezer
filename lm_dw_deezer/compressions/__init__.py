from .zip import zip_compress
from .gzip import gzip_compress
from .zstd import zstd_compress


__all__ = (
	'zip_compress',
	'gzip_compress',
	'zstd_compress'
)