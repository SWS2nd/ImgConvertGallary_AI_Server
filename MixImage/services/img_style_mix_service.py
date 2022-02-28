from ninja.files import UploadedFile
from ninja import File
import tensorflow as tf
import numpy as np
# 이미지 처리용(Pillow)
from PIL import Image
# opencv
import cv2
# util성 함수들은 utils app에서 관리
from MixImage.utils.utils import upload_tensor_img, load_style
from MixImage.apps import ImagedrawingstylemixConfig


# 사실상 핵심적인 서비스 함수 부분
# 사용자는 이미지 파일 이름, 이미지 파일, 화풍으로 사용할 이미지 모델을 넘겨 줬었음.
# 리턴은 s3에 올라간 변환된 이미지의 url(스트링)
def img_style_mix_apply(image_name: str, model_image_name: str,
                        image: UploadedFile = File(...),
                        model_image: UploadedFile = File(...)) -> str:

    # 1) 사용자 이미지 불러오기
    img = Image.open(image.file).convert('RGB')
    content_image = tf.keras.preprocessing.image.img_to_array(img)
    # 이미지 보기(이미지를 잘 불러왔는지 확인)
    # tf.keras.preprocessing.image.array_to_img(content_image).show()

    # 2) 사용자 이미지 전처리
    # float32 타입으로 바꾸고, newaxis 를 통해 배치 차원을 추가한 후에 255 로 나눠서 normalize 함
    # 이후 512, 512 으로 리사이즈
    #h, w, c = content_image.shape
    content_image_normalized = content_image.astype(np.float32)[np.newaxis, ...] / 255.
    content_image_resized = tf.image.resize(content_image_normalized, (512, 512))

    # 3) 화풍용 이미지 불러오기
    model_img = Image.open(model_image.file).convert('RGB')
    model_content_image = tf.keras.preprocessing.image.img_to_array(model_img)
    # 이미지 보기(이미지를 잘 불러왔는지 확인)
    # tf.keras.preprocessing.image.array_to_img(content_image2).show()

    # 4) 화풍용 이미지 전처리
    #h, w, c = content_image.shape
    model_image_normalized = model_content_image.astype(np.float32)[np.newaxis, ...] / 255.
    model_image_resized = tf.image.resize(model_image_normalized, (512, 512))

    # 5) 이미지 스타일 변환 모델에 리사이즈 한 사용자 이미지, 화풍용 이미지를 넣고 변환된 이미지를 돌려 받음
    # MixImage app의 apps.py의 ImagedrawingstylemixConfig 클래스의 hub_module 변수 이용
    # hub_module 변수는 텐서플로우 허브에서 이미지 스타일 변환 모델을 load 해놓은 변수
    # 즉, 이미지 스타일 변환 모델에 tf.constant()를 이용하여 리사이즈한 사용자 이미지, 화풍용 이미지를 넣고 결과 이미지를 받음
    # stylized_image는 정규화된 numpy array
    stylized_image = ImagedrawingstylemixConfig.hub_module(tf.constant(content_image_resized),
                                                                   tf.constant(model_image_resized))[0]

    # upload_tensor_img 함수는 s3 bucket에 변환된 이미지와 이미지명을 업로드 하고, 해당 이미지 경로를 return 해주는 함수
    # 첫번째 인자로 파일을 업로드 할 s3 bucket명,
    # 두번째 인자로 변환된 이미지(위 if문 중 어느 if문을 탔는지에 따라 s3 업로드 전 후처리 과정이 조금 다름),
    # 세번째 인자로 사용자로부터 받은 이미지명,
    # 네번째 인자로 이미지명에 덧붙일 drawing_style(s3에 저장시 파일명 : '현재날짜 현재시간_이미지명(drawing_style)')
    # 마지막 인자로 위쪽 if문 1, 2중 어느 if문을 탔는지(if style_route , elif style_path 중 어느 if문을 탔는지)
    # util성 함수들은 utils app에서 관리
    mixed_image_url = upload_tensor_img('testbucket777777', stylized_image, image_name, model_image_name)
    return mixed_image_url
