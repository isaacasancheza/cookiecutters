from base64 import b64encode
from dataclasses import dataclass
from json import dumps, loads
from typing import cast
from urllib.parse import urlencode

from aws_lambda_powertools.utilities.typing import LambdaContext
from lambda_ import handler

from tests import types


def request(
    path: str,
    route_key: str,
    /,
    *,
    body: types.Body | bytes | None = None,
    token: str | None = None,
    method: types.Method,
    params: types.Params | None = None,
    headers: types.Headers | None = None,
) -> types.Response:
    def lambda_context() -> LambdaContext:
        @dataclass
        class Context:
            function_name: str = 'test'
            memory_limit_in_mb: int = 128
            invoked_function_arn: str = (
                'arn:aws:lambda:us-east-1:123456789012:function:test'
            )
            aws_request_id: str = 'da658bd3-2d6f-4e7b-8ec2-937234644fdc'

        return cast(LambdaContext, Context())

    event = {
        'body': '{}',
        'headers': {},
        'rawPath': path,
        'routeKey': route_key,
        'requestContext': {
            'http': {
                'method': method,
            },
            'stage': '$default',
            'requestContext': {
                'http': {
                    'method': method,
                },
                'requestId': '227b78aa-779d-47d4-a48e-ce62120393b8',
            },
        },
    }

    if body:
        if isinstance(body, bytes):
            event['body'] = b64encode(body).decode()
            event['isBase64Encoded'] = True
        else:
            event['body'] = dumps(body)
    if token:
        event['headers']['Authorization'] = token
    if params:
        event['rawQueryString'] = urlencode(params)
        event['queryStringParameters'] = {
            key: value for key, value in params.items() if value
        }
    if headers:
        event['headers'].update(headers)
    response = handler(event, lambda_context())

    body = response.get('body', {})
    status_code = response['statusCode']

    if isinstance(body, str):
        body = loads(body)

    return status_code, cast(types.Body, body)


def get(
    path: str,
    route_key: str,
    /,
    *,
    token: str | None = None,
    params: types.Params | None = None,
    headers: types.Headers | None = None,
) -> types.Response:
    return request(
        path,
        route_key,
        token=token,
        method='GET',
        params=params,
        headers=headers,
    )


def put(
    path: str,
    route_key: str,
    /,
    *,
    body: types.Body | bytes,
    token: str | None = None,
    headers: types.Headers | None = None,
) -> types.Response:
    return request(
        path,
        route_key,
        body=body,
        method='PUT',
        token=token,
        headers=headers,
    )


def post(
    path: str,
    route_key: str,
    /,
    *,
    body: types.Body | bytes,
    token: str | None = None,
    headers: types.Headers | None = None,
) -> types.Response:
    return request(
        path,
        route_key,
        body=body,
        token=token,
        method='POST',
        headers=headers,
    )


def patch(
    path: str,
    route_key: str,
    /,
    *,
    body: types.Body,
    token: str | None = None,
    headers: types.Headers | None = None,
) -> types.Response:
    return request(
        path,
        route_key,
        body=body,
        token=token,
        method='PATCH',
        headers=headers,
    )


def delete(
    path: str,
    route_key: str,
    /,
    *,
    token: str | None = None,
    headers: types.Headers | None = None,
) -> types.Response:
    return request(
        path,
        route_key,
        token=token,
        method='DELETE',
        headers=headers,
    )
