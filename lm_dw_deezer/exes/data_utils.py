from pathlib import Path

from os import makedirs

from InquirerPy.base.control import Choice
from InquirerPy.prompts.list import ListPrompt


lm_dw_deezer_dir = '.lm_dw_deezer'
lm_dw_deezer_fn = 'data.json'

home_user = Path.home()

working_dir = f'{home_user}/{lm_dw_deezer_dir}'
makedirs(working_dir, exist_ok = True)
file_conf = f'{working_dir}/{lm_dw_deezer_fn}'

__browsers = ('firefox', 'manually')

l_browsers = ListPrompt(
	message = 'How you want to input your arl token:',
	choices = [
		Choice(
			value = 'firefox',
			name = 'Firefox'
		),
		Choice(
			value = 'manually',
			name = 'Manually'
		),
	],
	default = 'manually',
)