# /// script
# requires-python = ">={{ cookiecutter.python_version }}"
# dependencies = [
#     "aws-cdk-lib",
# ]
# ///
import aws_cdk as cdk
from stack import Stack

app = cdk.App()

Stack(
    app,
    'Stack',
    stack_name='{{cookiecutter.compute_stack_name}}',
    project_name='{{ cookiecutter.project_name  }}',
    sentry_dsn='',
    sentry_environment='',
)

app.synth()
