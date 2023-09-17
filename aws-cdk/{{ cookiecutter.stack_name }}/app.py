import aws_cdk as cdk
from pydantic_settings import BaseSettings, SettingsConfigDict

from stacks.root import RootStack


class Settings(BaseSettings):
    region: str
    account: str
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


app = cdk.App()
settings = Settings()

env = cdk.Environment(region=settings.region, account=settings.account)
RootStack(app, 'RootStack', stack_name='{{ cookiecutter.stack_name }}', env=env)

app.synth()
