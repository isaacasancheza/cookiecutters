from re import sub
from typing import Annotated

from app import patterns
from pydantic import (
    BeforeValidator,
    StringConstraints,
)

type String = Annotated[
    str,
    StringConstraints(
        min_length=1,
        strip_whitespace=True,
    ),
    BeforeValidator(
        lambda v: sub(r'\s+', ' ', v),
    ),
]
type SpanishLetters = Annotated[
    String,
    StringConstraints(
        pattern=patterns.SPANISH_LETTERS_PATTERN,
    ),
]
