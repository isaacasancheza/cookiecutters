from os import chdir
from pathlib import Path


files = [
    'app.py',
    'stacks',
    'chalice',
    'cdk.json',
]
folder = '{{ cookiecutter.stack_name }}'

chdir('..')
path = Path(folder)
for filename in files:    
    action = path.joinpath(filename)
    action.rename(f'./{filename}')
path.rmdir()
