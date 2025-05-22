import aws_cdk as cdk
from stack import Stack

app = cdk.App()

Stack(
    app,
    'Stack',
    stack_name='{{ cookiecutter.stack_name }}',
    project_name='{{ cookiecutter.project_name }}',
)

app.synth()
