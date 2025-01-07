from base64 import b64decode
from io import BytesIO
from typing import TypeVar

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.router import APIGatewayHttpRouter
from boto3.dynamodb.conditions import Key
from filetype import guess
from PIL import Image

from app import constants, services, settings
from app.api import exceptions
from app.database.models.images import Image as ImageModel
from app.database.tables import main_table
from app.integrations import s3

logger = Logger()
GenericImage = TypeVar('GenericImage', bound=ImageModel)


def get_image_from_body(
    router: APIGatewayHttpRouter,
    /,
    *,
    allowed_mime_types: list[str] = settings.IMAGE_ALLOWED_MIME_TYPES,
) -> tuple[Image.Image, str]:
    """Retrieve image from body and returns image, extension, and content type."""
    if not router.current_event.is_base64_encoded or not router.current_event.body:
        logger.error('Empty body received')
        raise exceptions.UnsupportedMediaTypeError
    try:
        body = b64decode(
            router.current_event.body,
            validate=True,
        )
    except Exception as _:
        logger.error('Could not decode body')
        raise exceptions.UnsupportedMediaTypeError
    type = guess(body)
    if not type:
        logger.error('Could not determine type')
        raise exceptions.UnsupportedMediaTypeError
    if type.MIME not in allowed_mime_types:
        logger.error('Unsupported media type')
        raise exceptions.UnsupportedMediaTypeError
    image = Image.open(BytesIO(body))
    format = image.format or type.MIME.replace('image/', '')
    format = format.lower()
    return image, format


def upload(
    image: Image.Image,
    image_model: ImageModel,
) -> None:
    with BytesIO() as buffer:
        image.save(buffer, image_model.format)
        buffer.seek(0)
        s3.put_object(
            Key=image_model.key,
            Body=buffer,
            Bucket=image_model.bucket,
            ContentType=image_model.content_type,
            Metadata=image_model.metadata,
        )


def thumbnail(
    image: Image.Image,
    /,
    *,
    min_width: int,
    min_height: int,
    max_width: int,
    max_height: int,
) -> Image.Image:
    """Resizess image to the given constraints."""
    if image.width < min_width or image.height < min_height:
        logger.error('Image is too small')
        raise exceptions.ValidationError('body', 'image_too_small')

    if image.width > max_width or image.height > max_height:
        image.thumbnail((max_width, max_height))

    return image


def cleanup(
    images: list[GenericImage],
    /,
) -> None:
    """Deletes all given images."""
    keys = []
    with main_table.batch_writer() as batch:
        for image in images:
            batch.delete_item(
                Key={
                    'pk': getattr(image, 'pk'),
                    'sk': getattr(image, 'sk'),
                },
            )
            # append s3 key
            keys.append(image.key)
    # delete from s3
    services.s3.batch_delete_objects(
        keys=keys,
        bucket_name=settings.CDN_BUCKET_NAME,
    )


def query_and_cleanup(
    *,
    model: type[GenericImage],
    partition_key: str,
    current_image_keys: tuple[str, str] | None = None,
) -> None:
    """Deletes all images except current."""
    images = main_table.query(
        KeyConditionExpression=Key('pk').eq(partition_key)
        & Key('sk').begins_with(constants.KeyPrefix.IMAGE),
    )['Items']
    current_image_pk, current_image_sk = current_image_keys or (None, None)
    images = [
        model.model_validate(image)
        for image in images
        if image['pk'] != current_image_pk and image['sk'] != current_image_sk
    ]
    cleanup(images)


def query_and_split_in_to_delete_and_to_preserve(
    *,
    model: type[GenericImage],
    keep_images: list[GenericImage],
    partition_key: str,
) -> tuple[list[GenericImage], list[GenericImage]]:
    """Retrieve images and split images to be deleted and images to be keep."""
    to_delete: list[GenericImage] = []
    to_preserve: list[GenericImage] = []
    keep_image_ids = [image.id for image in keep_images]

    existing_images = main_table.query(
        KeyConditionExpression=Key('pk').eq(partition_key)
        & Key('sk').begins_with(constants.KeyPrefix.IMAGE),
    )['Items']

    for existing_image in existing_images:
        existing_image = model.model_validate(existing_image)
        if existing_image.id in keep_image_ids:
            to_preserve.append(existing_image)
        else:
            to_delete.append(existing_image)

    return to_delete, to_preserve
