from django.core.files.storage import default_storage

from .models import Image  # 실제 Image 모델 경로에 맞게 수정
from django.core.files.uploadedfile import UploadedFile


def upload_image(user, image_file, ref_type: str, ref_id: int) -> Image:
    """
    S3에 이미지 저장 후 URL 추출해서 Image 모델 저장
    """
    # 1. S3에 저장
    file_path = default_storage.save(image_file.name, image_file)

    # 2. URL 생성
    url = default_storage.url(file_path)

    # 3. DB 저장
    return Image.objects.create(
        user=user,
        ref_type=ref_type,
        ref_id=ref_id,
        url=url
    )