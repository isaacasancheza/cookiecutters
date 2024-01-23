from json import dumps, loads
from typing import cast
from dataclasses import dataclass
from urllib.parse import urlencode

from pytest import fixture

from api.resolver import handler
from tests import typing


@fixture
def lambda_context() -> typing.LambdaContext:
    @dataclass
    class FakeLambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = "arn:aws:lambda:us-east-1:123456789012:function:test"
        aws_request_id: str = "da658bd3-2d6f-4e7b-8ec2-937234644fdc"

    return cast(typing.LambdaContext, FakeLambdaContext())


@fixture
def lambda_handler(lambda_context: typing.LambdaContext) -> typing.LambdaHandler:
    def _lambda_handler(
            path: str,
            /, 
            *,
            body: typing.Body = {},
            method: typing.Method = 'GET',
            params: typing.Params = {}, 
        ) -> typing.Response:
        event = {
            'body': '{}',
            'rawPath': path,
            'requestContext': {
                'http': {
                    'method': method,
                },
                'stage': '$default',
                'requestContext': {
                    'http': {
                        'method': method,
                    },
                    'requestId': '227b78aa-779d-47d4-a48e-ce62120393b8',  # correlation ID
                },
            },
        }
        if body:
            event['body'] = dumps(body)
        if params:
            event['rawQueryString'] = urlencode(params)
            event['queryStringParameters'] = {key: value for key, value in params.items()}

        response = handler(event, lambda_context)

        body = response.get('body', '{}')
        status_code = response['statusCode']

        return status_code, loads(cast(str, body))
    return _lambda_handler


@fixture
def get(lambda_handler: typing.LambdaHandler) -> typing.Get:
    def _get(
            path: str,
            /,
            *,
            params: typing.Params = {},
        ) -> typing.Response:
        return lambda_handler(path, params=params)
    return _get


@fixture
def put(lambda_handler: typing.LambdaHandler) -> typing.Put:
    def _put(
            path: str,
            body: typing.Body,
            /,
        ) -> typing.Response:
        return lambda_handler(path, method='PUT', body=body)
    return _put


@fixture
def post(lambda_handler: typing.LambdaHandler) -> typing.Post:
    def _post(
            path: str,
            body: typing.Body,
            /,
        ) -> typing.Response:
        return lambda_handler(path, method='POST', body=body)
    return _post


@fixture
def delete(lambda_handler: typing.LambdaHandler) -> typing.Delete:
    def _delete(
            path: str,
            /,
        ) -> typing.Response:
        return lambda_handler(path, method='DELETE')
    return _delete
