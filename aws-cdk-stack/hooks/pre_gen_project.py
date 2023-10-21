from os.path import exists


files = [
    '{{ cookiecutter.nested_stack_name }}.py',
]

for filename in files:
    if exists(f'../{filename}'):
        print(f'filename "{filename}" already exists')
        exit(1)
