from os.path import exists


files = [
    'app.py',
    'stacks',
    'chalice',
    'cdk.json',
]

for filename in files:
    if exists(f'../{filename}'):
        print(f'filename "{filename}" already exists')
        exit(1)
