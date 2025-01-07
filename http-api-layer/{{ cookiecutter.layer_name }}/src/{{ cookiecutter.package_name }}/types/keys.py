from pydantic import StringConstraints


class Key(StringConstraints):
    def __init__(
        self,
        prefix: str,
        unique_identifier: str = r'[a-z0-9-]{36}',
        /,
    ) -> None:
        super().__init__(pattern=rf'^{prefix}{unique_identifier}$')
