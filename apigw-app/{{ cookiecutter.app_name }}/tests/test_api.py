from tests import typing


def test_api(
        get: typing.Get,    
    ):
    status, response = get('/nonexistingroute')

    assert status == 404
    assert response == {
        'message': 'Not found',
        'statusCode': 404, 
    }
