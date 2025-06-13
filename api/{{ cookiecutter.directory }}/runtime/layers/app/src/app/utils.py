from base64 import b64decode, b64encode
from json import dumps, loads
from typing import cast
from uuid import uuid4
from datetime import datetime, timezone

from app import constants

def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def encode_tuple(
    tupla: tuple[str, str],
    /,
) -> str:
    """Encodes tuple as base64."""
    return b64encode(
        dumps(
            tupla,
        ).encode(),
    ).decode()


def decode_tuple(
    encrypted_string: str,
    /,
) -> tuple[str, str]:
    """Decodes bas64 encoded tuple."""
    try:
        result = loads(
            b64decode(
                encrypted_string,
                validate=True,
            ),
        )
        if not isinstance(result, list):
            return '', ''
        if len(result) != 2:
            return '', ''
        if not isinstance(result[0], str) or not isinstance(result[1], str):
            return '', ''
        return cast(tuple[str, str], result)
    except Exception as _:
        return '', ''


def generate_sk(
    prefix: constants.KeyPrefix,
    /,
) -> str:
    return f'{prefix}{uuid4()}'
