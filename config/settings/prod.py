from .base import * # noqa
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False   # 디버그 모드(개발 모드) 에러가 발생 하면 장고에서 노란 화면으로 알려줌

ALLOWED_HOSTS = [
    "3.93.163.29", # EC2 퍼블릭 IP
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


dsn = os.getenv("SENTRY_DSN")  # .env.prod에서 불러옴

if dsn:
    sentry_sdk.init(
        dsn=dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,  # 퍼포먼스 추적 (조절 가능)
        send_default_pii=True    # 사용자 IP 등 기본 정보 포함
    )