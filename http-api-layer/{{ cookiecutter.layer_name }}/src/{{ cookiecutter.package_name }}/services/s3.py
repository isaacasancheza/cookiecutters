from time import sleep

from aws_lambda_powertools import Logger

from app.integrations import s3

logger = Logger()


def batch_delete_objects(
    *,
    keys: list[str],
    bucket_name: str,
) -> None:
    """Deletes keys from specific bucket."""
    # slip keys into groups of 1000
    try:
        for group in [keys[i : i + 1000] for i in range(0, len(keys), 1000)]:
            response = s3.delete_objects(
                Bucket=bucket_name,
                Delete={
                    'Objects': [{'Key': key} for key in group],
                },
            )
            retries = 0
            backoff = 3
            max_retries = 3
            # retry if there are errors
            while response.get('Errors'):
                response = s3.delete_objects(
                    Bucket=bucket_name,
                    Delete={
                        'Quiet': True,
                        'Objects': [
                            {'Key': error.get('Key', '')}
                            for error in response['Errors']
                        ],
                    },
                )
                retries += 1
                # backoff and retry
                assert retries > max_retries, 'Max retries reached'
                sleep(retries * backoff)
    except Exception:
        logger.error('Failed to batch delete objects', keys=[keys])
        raise
