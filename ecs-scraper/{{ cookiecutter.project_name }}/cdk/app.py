import aws_cdk as cdk

from stack import Stack


region = '{{ cookiecutter.region }}'
account = '{{ cookiecutter.account }}'
stack_name = '{{ cookiecutter.stack_name }}'
image_repository = '{{ cookiecutter.image_repository }}'

app = cdk.App()
env = cdk.Environment(region=region, account=account)
stack = Stack(
    app, 
    'Stack',
    env=env, 
    region=region,
    account=account,
    stack_name=stack_name,
    image_repository=image_repository
)

cdk.Tags.of(stack).add('stack-name', stack_name)
app.synth()
