from os.path import exists


files = [
    '{{ cookiecutter.stack_name }}.py',
]

for filename in files:
    if exists(f'../{filename}'):
        print(f'filename "{filename}" already exists')
        exit(1)
