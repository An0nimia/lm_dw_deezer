from os import makedirs

from pathlib import Path

from InquirerPy.base.control import Choice
from InquirerPy.prompts.list import ListPrompt

from ..config.utils_infos import LM_DW_DEEZER_DIR


lm_dw_deezer_fn = 'data.json'

home_user = Path.home()

working_dir = f'{home_user}/{LM_DW_DEEZER_DIR}'
makedirs(working_dir, exist_ok = True)
file_conf = f'{working_dir}/{lm_dw_deezer_fn}'

__browsers = ('firefox', 'manually')

choices = [
	Choice(
		value = browser,
		name = browser.capitalize()
	)

	for browser in __browsers
]

l_browsers = ListPrompt(
	message = 'How you want to input your arl token:',
	choices = choices,
	default = 'manually',
)