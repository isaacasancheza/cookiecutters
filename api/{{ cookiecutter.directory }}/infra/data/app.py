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
    stack_name='{{ cookiecutter.data_stack_name }}',
    project_name='{{ cookiecutter.project_name }}',
    removal_policy=cdk.RemovalPolicy.DESTROY,
)

app.synth()
