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
    api_name='{{ cookiecutter.project_name }}',
    api_domain_name='',
    api_domain_zone_name='',
    api_domain_record_name='',
    api_domain_hosted_zone_id='',
    api_domain_name_certificate_arn='',
    param_api_cors_allow_origin='',
)

app.synth()
