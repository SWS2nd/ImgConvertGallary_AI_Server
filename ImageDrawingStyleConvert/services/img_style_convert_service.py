from ninja.files import UploadedFile
from ninja import File
import tensorflow as tf
import numpy as np
# 이미지 처리용(Pillow)
from PIL import Image
# opencv
import cv2
# util성 함수들은 utils app에서 관리
from ImageDrawingStyleConvert.utils.utils import upload_tensor_img, load_style
from ImageDrawingStyleConvert.apps import ImagedrawingstyleconvertConfig


# 사실상 핵심적인 서비스 함수 부분
# 사용자는 이미지 파일 이름, 이미지 파일, 화풍으로 사용할 모델 type을 넘겨 줬었음.
# 리턴은 s3에 올라간 변환된 이미지의 url(스트링)
def img_style_convert_apply(image_name: str, model_type: str, image: UploadedFile = File(...)) -> str:
    # 아래서 사용할 변수 초기화
    style_route = ''
    style_path = ''
    stylized_image = ''
    conditional_number = ''

    # 화풍용 이미지 불러오기
    # 1. static/models 내에 저장된 화풍용 이미지(.t7으로 저장된)를 모델로 사용하는 경우,
    if model_type == 'la_muse':
        style_route = 'static/models/eccv16/la_muse.t7'
    elif model_type == 'composition':
        style_route = 'static/models/eccv16/composition_vii.t7'
    elif model_type == 'starry_night':
        style_route = 'static/models/eccv16/starry_night.t7'
    elif model_type == 'the_wave':
        style_route = 'static/models/eccv16/the_wave.t7'
    elif model_type == 'candy':
        style_route = 'static/models/instance_norm/candy.t7'
    elif model_type == 'feathers':
        style_route = 'static/models/instance_norm/feathers.t7'
    elif model_type == 'mosaic':
        style_route = 'static/models/instance_norm/mosaic.t7'
    elif model_type == 'the_scream':
        style_route = 'static/models/instance_norm/the_scream.t7'
    elif model_type == 'udnie':
        style_route = 'static/models/instance_norm/udnie.t7'
    # 2. 웹에서 화풍용 이미지를 가져와 사용자 이미지와 텐서플로우 허브의 이미지 스타일 변환 모델로 통과시키는 경우
    # 화풍용 이미지로 사용할 이미지는 크기가 모두 다르므로 resize 필요
    elif model_type == 'kandinsky':
        # 텐서플로우 케라스 utils의 get_file() 함수를 이용함
        # 화풍용 이미지로 칸딘스키 이미지 파일 사용시
        style_path = tf.keras.utils.get_file('kandinsky5.jpg',
                                             'https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg')
    elif model_type == 'your_name_animation':
        style_path = tf.keras.utils.get_file('your_name_animation.jpg',
                                             'https://t1.daumcdn.net/cfile/tistory/2133AC485870B74D32')

    # 사용자 이미지 불러오기
    img = Image.open(image.file).convert('RGB')
    content_image = tf.keras.preprocessing.image.img_to_array(img)
    # 이미지 보기(이미지를 잘 불러왔는지 확인)
    # tf.keras.preprocessing.image.array_to_img(content_image).show()

    # 1. ----- static/models 안의 저장된 화풍용 이미지를 사용하는 경우 -----
    if style_route:
        # if style_route 조건문을 탈 시
        # 마지막 s3 업로드 함수의 인자로 사용할 변수
        conditional_number = 1

        # 1) 사용자 이미지 전처리(open cv 이용시)
        h, w, c = content_image.shape
        img = cv2.resize(content_image, dsize=(500, int(h / w * 500)))
        MEAN_VALUE = [103.939, 116.779, 123.680]
        blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)
        # print(blob.shape)

        # 2) 화풍용 이미지를 불러와 전처리 된 사용자 이미지와 mix
        net = cv2.dnn.readNetFromTorch(style_route)
        net.setInput(blob)
        output = net.forward()

        # 3) 후처리
        stylized_image = output.squeeze().transpose((1, 2, 0))
        stylized_image += MEAN_VALUE
        stylized_image = np.clip(stylized_image, 0, 255)
        # BGR 순서로 되어 있는 것으로 보임. 따라서, 업로드 전 RGB 순서로 바꿔야 함
        # numpy.ndarray type(opencv를 이용했고, 0~1 소수점 즉, 정규화 된 값이 아님)
        stylized_image = stylized_image.astype('uint8')

        # 이미지 보기(최종 후처리 된 이미지 확인)
        # imshow로 볼 경우, 볼 이미지가 BGR, RGB 인지 확인
        # cv2.imshow('stylized_image', stylized_image)
        # cv2.waitKey(0)

    # 2. ----- 웹에서 화풍용 이미지를 가져와 사용자 이미지와 텐서플로우 허브의 이미지 스타일 변환 모델로 통과시키는 경우 -----
    elif style_path:
        # elif style_path 조건문을 탈 시
        # 마지막 s3 업로드 함수의 인자로 사용할 변수
        conditional_number = 2

        # 1) 화풍용 이미지 전처리
        # load_style 함수는 비율을 유지하면서 스타일 이미지 크기를 줄이는 함수
        # 스타일도 위처럼 읽어와도 되지만, 스타일은 비율이 유지되어야만 올바르게 적용됨
        # 스타일 비율도 일괄적으로 resizing 할 경우 결과가 이상할 수 있음에 유의
        # 두번째 인자는 이미지의 최대 크기를 제한하고자 하는 길이
        # util성 함수들은 utils app에서 관리
        style_image = load_style(style_path, 512)

        # 2) 사용자 이미지 전처리
        # float32 타입으로 바꾸고, newaxis 를 통해 배치 차원을 추가한 후에 255 로 나눠서 normalize 함
        # 이후 512, 512 으로 리사이즈
        content_image_normalized = content_image.astype(np.float32)[np.newaxis, ...] / 255.
        content_image_resized = tf.image.resize(content_image_normalized, (512, 512))

        # 3) 이미지 스타일 변환 모델에 리사이즈 한 사용자 이미지, 화풍용 이미지를 넣고 변환된 이미지를 돌려 받음
        # ImageDrawingStyleConvert app의 apps.py의 ImagedrawingstyleconvertConfig 클래스의 hub_module 변수 이용
        # hub_module 변수는 텐서플로우 허브에서 이미지 스타일 변환 모델을 load 해놓은 변수
        # 즉, 이미지 스타일 변환 모델에 tf.constant()를 이용하여 리사이즈한 사용자 이미지, 화풍용 이미지를 넣고 결과 이미지를 받음
        # stylized_image는 정규화된 numpy array
        stylized_image = ImagedrawingstyleconvertConfig.hub_module(tf.constant(content_image_resized),
                                                                   tf.constant(style_image))[0]

    # upload_tensor_img 함수는 s3 bucket에 변환된 이미지와 이미지명을 업로드 하고, 해당 이미지 경로를 return 해주는 함수
    # 첫번째 인자로 파일을 업로드 할 s3 bucket명,
    # 두번째 인자로 변환된 이미지(위 if문 중 어느 if문을 탔는지에 따라 s3 업로드 전 후처리 과정이 조금 다름),
    # 세번째 인자로 사용자로부터 받은 이미지명,
    # 네번째 인자로 이미지명에 덧붙일 drawing_style(s3에 저장시 파일명 : '현재날짜 현재시간_이미지명(drawing_style)')
    # 마지막 인자로 위쪽 if문 1, 2중 어느 if문을 탔는지(if style_route , elif style_path 중 어느 if문을 탔는지)
    # util성 함수들은 utils app에서 관리
    stylized_image_url = upload_tensor_img('image-style-convert-bucket', stylized_image, image_name, model_type,
                                           conditional_number)
    return stylized_image_url
