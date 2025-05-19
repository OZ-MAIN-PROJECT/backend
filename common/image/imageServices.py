import uuid
from urllib.parse import urlparse, unquote

import boto3
from django.core.files.storage import default_storage
from django.conf import settings

from .models import Image


def upload_image(user, image_file, ref_type: str, ref_id: int) -> Image:
    """
    S3에 이미지 저장 후 URL 추출해서 Image 모델 저장
    """
    # 경로 지정: community/EMOTION/1/파일명.jpg
    filename = f"{uuid.uuid4().hex}_{image_file.name}"
    path = f"community/{ref_type}/{ref_id}/{filename}"
    saved_path = default_storage.save(path, image_file)
    url = default_storage.url(saved_path)

    # 3. DB 저장
    # image만 받고 뒤에 오는 두 번째 값(즉 created)은 필요 없으니까 _로 버리는 것이에요
    image, _ = Image.objects.update_or_create(
        ref_type=ref_type,
        ref_id=ref_id,
        defaults={
            'user': user,
            'url': url
        }
    )
    return image

def delete_image_from_s3(file_url):
    """
    S3 전체 URL에서 key 추출 후 삭제
    예: https://bucket.s3.amazonaws.com/community/EMOTION/1/file.jpg → key: community/EMOTION/1/file.jpg
    """
    s3 = boto3.client('s3')
    bucket = settings.AWS_STORAGE_BUCKET_NAME  # ✅ 올바르게 가져옴

    parsed_url = urlparse(file_url)
    raw_key = parsed_url.path.lstrip('/')
    key = unquote(raw_key)

    print(f"Deleting from bucket={bucket}, key={key}")  # ✅ 이제 문자열 출력됨

    s3.delete_object(Bucket=bucket, Key=key)