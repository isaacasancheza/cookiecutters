from os import environ

from aws_lambda_powertools.utilities.parameters import get_parameters

PROJECT_NAME = environ['PROJECT_NAME']
PARAMETERS = get_parameters(f'/{PROJECT_NAME}', decrypt=True)

# cdn
CDN_DOMAIN_NAME = PARAMETERS['cdn/domain-name']

# storage
MAIN_BUCKET_NAME = PARAMETERS['storage/main-bucket/name']

# database
MAIN_TABLE_NAME = PARAMETERS['database/main-table/name']

# authentication
USER_POOL_ID = PARAMETERS['authentication/user-pool/id']
USER_POOL_REGION = PARAMETERS['authentication/user-pool/region']
USER_POOL_CLIENT_ID = PARAMETERS['authentication/user-pool-client/id']
