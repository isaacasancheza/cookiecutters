from os.path import exists
from os import listdir


filename = '{{ cookiecutter.action_name }}.yaml'
if exists('../%s' % filename):
    print('Filename "%s" already exists' % filename)
    exit(1)
