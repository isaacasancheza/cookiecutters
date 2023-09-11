from os import getenv

import aws_cdk as cdk

from stacks.root import RootStack


app = cdk.App()
env = cdk.Environment(account=getenv('ACCOUNT'), region=getenv('REGION'))

RootStack(app, 'RootStack', stack_name='{{ cookiecutter.stack_name }}', env=env)

app.synth()
