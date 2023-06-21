def handler(event, _):
    record, = event['Records']

    request = record['cf']['request']
    uri = request['uri']

    if uri.endswith('/'):
        request['uri'] += 'index.html'
    elif '.' not in uri:
        request['uri'] += '/index.html'

    return request
