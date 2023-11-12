from api_deezer_full.gw.types import Contributors

from api_deezer_full.pipe.types import Synchronized_Line


def lyric_w_time(synchronized_lines: list[Synchronized_Line]) -> str:
	infos_sync = [
		f'{info_sync.lrcTimestamp}{info_sync.line}'
		for info_sync in synchronized_lines
	]

	return '\n'.join(infos_sync)


def get_contributors(contributors: Contributors):
	res: list[tuple[str, str]] = []

	for contributor in contributors:
		if contributor.role == 'artist':
			continue

		res.append(
			(contributor.role, contributor.name)
		)

	return res


def get_composers(contributors: Contributors):
	composers: list[str] = []

	for contributor in contributors:
		if contributor.role == 'composer':
			composers.append(contributor.name)

	return composers


def generate_rgain(gain: float) -> float:
    return (
		(gain + 18.4) * -1
	)