import os
import shutil


stack_name = '{{ cookiecutter.stack_name }}'
for file in os.listdir():
    shutil.move(file, '..')

os.chdir('..')
os.rmdir(stack_name)
