from os import chdir
from pathlib import Path

files = [
    'template.yaml',
    'samconfig.toml',
    'parameter-overrides.bash',
]
folder = '{{ cookiecutter.__static_name }}'

chdir('..')
path = Path(folder)
for filename in files:    
    action = path.joinpath(filename)
    action.rename('./%s' % filename)
path.rmdir()
