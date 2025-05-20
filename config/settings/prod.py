from .base import * # noqa

# 파일 업로드 설정
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEBUG = False   # 디버그 모드(개발 모드) 에러가 발생 하면 장고에서 노란 화면으로 알려줌

ALLOWED_HOSTS = [
    "3.93.163.29", "localhost", "127.0.0.1", "127.0.0.1:8000", "sussyoo.kro.kr"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DjangoMain',
        'USER': 'dev_user',
        'PASSWORD': 'securepassword',
        'HOST': 'djangomain.ckpawa0qerlm.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}