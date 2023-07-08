from os.path import exists
from os import listdir


files = [
    'template.yaml',
    'samconfig.toml',
    'parameter-overrides.bash',
]

for filename in files:
    if exists('../%s' % filename):
        print('filename "%s" already exists' % filename)
        exit(1)
