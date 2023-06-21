from os import chdir
from pathlib import Path


action_name = '{{ cookiecutter.action_name }}'

chdir('..')
path = Path(action_name)
action = path.joinpath('%s.yaml' % action_name)
action.rename('./%s.yaml' % action_name)
path.rmdir()
