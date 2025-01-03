#!/usr/bin/env -S uv run
import aws_cdk as cdk
from stack import Stack

app = cdk.App()

Stack(
    app,
    'Stack',
    stack_name={{ cookiecutter.stack_name }},
)

app.synth()
