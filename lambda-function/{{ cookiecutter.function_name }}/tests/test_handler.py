import lambda_


def test_handler(
    lambda_context,
):
    event = {}
    assert lambda_.handler(event, lambda_context) is None
