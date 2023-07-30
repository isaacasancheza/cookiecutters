from os import chdir
from pathlib import Path


files = [
    '{{ cookiecutter.stack_name}}.py',
]
folder = '{{ cookiecutter.stack_name }}'

chdir('..')
path = Path(folder)
for filename in files:    
    action = path.joinpath(filename)
    action.rename(f'./{filename}')
path.rmdir()
