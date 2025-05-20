import uuid
from urllib.parse import urlparse, unquote
import boto3

from django.core.files.storage import default_storage
from django.conf import settings
from .models import Image


def upload_image(user, image_file, ref_type: str, ref_id: int) -> Image:
    try:
        filename = f"{uuid.uuid4().hex}_{image_file.name}"
        path = f"community/{ref_type}/{ref_id}/{filename}"
        saved_path = default_storage.save(path, image_file)
        url = default_storage.url(saved_path)

        print(f"✅ saved_path: {saved_path}")
        print(f"✅ url: {url}")

        if not url.startswith("http"):
            raise RuntimeError("Invalid image upload URL")

        image, _ = Image.objects.update_or_create(
            ref_type=ref_type,
            ref_id=ref_id,
            defaults={'user': user, 'url': url}
        )
        return image
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        raise



def delete_image_from_s3(file_url: str) -> None:
    """
    S3 URL에서 key 추출 후 삭제
    """
    if settings.AWS_S3_CUSTOM_DOMAIN not in file_url:
        raise ValueError("Invalid S3 file URL")

    parsed_url = urlparse(file_url)
    key = unquote(parsed_url.path.lstrip('/'))

    print(f"🗑️ Deleting from S3: bucket={settings.AWS_STORAGE_BUCKET_NAME}, key={key}")

    s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
    s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
