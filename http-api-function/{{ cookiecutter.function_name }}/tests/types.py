from typing import Any, Literal

type Body = dict[str, Any]
type Params = dict[str, Any]
type Method = Literal['GET', 'PUT', 'POST', 'PATCH', 'DELETE']
type Headers = dict[str, Any]
type Response = tuple[int, dict[str, Any]]
