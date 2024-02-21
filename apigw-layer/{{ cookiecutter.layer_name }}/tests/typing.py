from typing import (
    Any as _Any,
    Literal as _Literal,
    Protocol as _Protocol,
)

from api import typing as api_typing
from aws_lambda_powertools.utilities.typing import LambdaContext


type Body = dict[str, _Any]
type Params = dict[str, _Any]
type Method = _Literal['GET', 'PUT', 'POST', 'DELETE']
type Response = tuple[int, dict[str, _Any]]


class Get(_Protocol):
    def __call__(
            self,
            path: str,
            /, 
            *,
            params: Params = {},
        ) -> Response:
        ...


class Put(_Protocol):
    def __call__(
            self,
            path: str,
            body: Body,
            /, 
        ) -> Response:
        ...


class Post(_Protocol):
    def __call__(
            self,
            path: str,
            body: Body,
            /, 
        ) -> Response:
        ...


class Delete(_Protocol):
    def __call__(
            self,
            path: str,
            /, 
        ) -> Response:
        ...


class LambdaHandler(_Protocol):
    def __call__(
            self, 
            path: str, 
            /, 
            *,
            body: Body = {},  
            method: Method = 'GET',
            params: Params = {},
        ) -> Response:
        ...
