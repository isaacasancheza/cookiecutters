from lambda_ import handler


def test_handler(
    lambda_context,
):
    event = {}
    assert handler(event, lambda_context) is None
