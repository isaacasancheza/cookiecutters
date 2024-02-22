#!/usr/bin/env python3
from os import environ

import sentry_sdk
from aws_lambda_powertools import Logger

sentry_sdk.init(
    dsn=environ['SENTRY_DSN'],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

logger = Logger()
