from os import environ
from pathlib import Path

from aws_lambda_powertools.utilities.parameters import get_parameters
from botocore.config import Config

DEV = bool(environ.get('POWERTOOLS_DEV'))
SRC_DIR = Path(__file__).parent

PROJECT_NAME = environ['PROJECT_NAME']
PARAMETERS = get_parameters(f'/{PROJECT_NAME}', decrypt=True)

# boto3 config
BOTO3_CONFIG = Config(
    retries={
        'mode': 'standard',
        'max_attempts': 8,
    },
)

# cdn
CDN_DOMAIN_NAME = PARAMETERS['cdn/domain-name']

# storage
MAIN_BUCKET_NAME = PARAMETERS['storage/main-bucket/name']
CDN_BUCKET_NAME = PARAMETERS['storage/cdn-bucket/name']

# database
MAIN_TABLE_NAME = PARAMETERS['database/main-table/name']

# api
CORS_ALLOW_ORIGIN = PARAMETERS['api/cors-allow-origin']

# authentication
USER_POOL_ID = PARAMETERS['authentication/user-pool/id']
USER_POOL_REGION = PARAMETERS['authentication/user-pool/region']
USER_POOL_CLIENT_ID = PARAMETERS['authentication/user-pool-client/id']
