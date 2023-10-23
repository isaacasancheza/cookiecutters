from os.path import exists


files = [
    'app.py',
    'stack.py',
    'cdk.json',
    'nested_stacks',
]

for filename in files:
    if exists(f'../{filename}'):
        print(f'filename "{filename}" already exists')
        exit(1)
