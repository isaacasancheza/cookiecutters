def handler(event, _):
    record, = event['Records']
    request = record['cf']['request']

    if 'headers' not in request:
        return request
    
    headers = request['headers']

    if 'host' not in headers:
        return request

    for host in headers['host']:
        if 'cloudfront.net' in host['value']:
            return {
                'status': 404,
                'statusDescription': 'Page not found',
                'headers': {
                    'content-type': [
                        { 
                            'key': 'Content-Type',
                            'value': 'text/plain; charset=UTF-8',
                        },
                    ],
                    'cache-control': [
                        {
                            'key': 'Cache-Control',
                            'value': 'public, max-age=31536000, s-maxage=86400, immutable',
                        },
                    ],
                },
            }

    return request
