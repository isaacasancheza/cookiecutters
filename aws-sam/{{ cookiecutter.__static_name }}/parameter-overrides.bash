#!/usr/bin/env bash
params=(
)

script=`cat << EOF
from re import match
from sys import argv


params = '${params[@]}'.split()

for param in params:
    assert match(r'^\w+=\w+$', param), 'invalid parameter: %s' % param

assert params, 'No enough parameters'

params = ','.join(params)

print('--parameter-overrides ' + params)
EOF
`
python -c "$script"
