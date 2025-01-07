from aws_lambda_powertools.event_handler.exceptions import ServiceError
from aws_lambda_powertools.event_handler.openapi.exceptions import ValidationException


class NotFoundError(ServiceError):
    def __init__(self, message: str = 'Not Found'):
        super().__init__(404, message)


class ForbiddenError(ServiceError):
    def __init__(self, message: str = 'Forbidden'):
        super().__init__(403, message)


class BadRequestError(ServiceError):
    def __init__(self, message: str = 'Bad Request'):
        super().__init__(400, message)


class ValidationError(ValidationException):
    def __init__(self, type: str, loc: str, *locs: str):
        errors = [
            {
                'loc': (loc,) + locs,
                'type': type,
            },
        ]
        super().__init__(errors)


class UnauthorizedError(ServiceError):
    def __init__(self):
        super().__init__(401, 'Unauthorized')


class TooManyRequestsError(ServiceError):
    def __init__(self):
        super().__init__(429, 'Too Many Requests')


class UnsupportedMediaTypeError(ServiceError):
    def __init__(self):
        super().__init__(415, 'Unsupported Media Type')
