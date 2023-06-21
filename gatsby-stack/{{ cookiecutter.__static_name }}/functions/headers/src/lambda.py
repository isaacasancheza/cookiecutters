def handler(event, _):
    """
    Add security and cache headers
    """
    record, = event['Records']

    request = record['cf']['request']
    response = record['cf']['response']

    uri = request['uri']

    # https://www.gatsbyjs.com/docs/how-to/previews-deploys-hosting/caching/
    # https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html#ExpirationDownloadDist
    if (uri.startswith('/static/') or uri.endswith('.js') or uri.endswith('.js.map') or uri.endswith('.css')) and not uri.endswith('/sw.js'):
        response['headers']['cache-control'] = [
            {
                'key': 'Cache-Control',
                'value': 'public, max-age=31536000, s-maxage=86400, immutable',
            }
        ]
    else:
        response['headers']['cache-control'] = [
            {
                'key': 'Cache-Control',
                'value': 'cache-control: public, max-age=0, s-maxage=86400, must-revalidate',
            }
        ]

    return response
