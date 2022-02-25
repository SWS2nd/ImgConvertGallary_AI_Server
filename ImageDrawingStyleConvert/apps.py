from django.apps import AppConfig
import boto3
import tensorflow_hub as hub
from .my_apps import s3_settings


class ImagedrawingstyleconvertConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ImageDrawingStyleConvert'
    # 텐서플로우 허브 관련 코드(이미지 스타일 변환 모델을 텐서플로우 허브에서 불러와 놓는 작업)
    hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    # s3 관련 코드
    # secret 으로 빼놓고 해당 파일은 .gitignore를 해도 좋지만, github 레포를 그냥 private 으로 설정하는 것을 추천 (배포 과정이 더 간단해짐)
    # s3 = boto3.client('s3', aws_access_key_id='AKIA44BSPAIR7QQTW77G',
    #                   aws_secret_access_key='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', region_name='ap-northeast-2')
    s3 = s3_settings
