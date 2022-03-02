import numpy as np
# 이미지 처리용
from PIL import Image
# 파일 형태로 만들어서 s3에 업로드용
from io import BytesIO
from MixImage.apps import ImagedrawingstylemixConfig
# s3에 저장할 이미지명에 붙일 날짜, 시간용
from datetime import datetime


# upload_tensor_img 함수는 s3 bucket에 변환된 이미지와 이미지명을 업로드 하는 함수
# 첫번째 인자로 파일을 업로드 할 s3 bucket명,
# 두번째 인자로 변환된 이미지(위 if문 중 어느 if문을 탔는지에 따라 s3 업로드 전 후처리 과정이 조금 다름),
# 세번째 인자로 사용자로부터 받은 이미지명,
# 네번째 인자로 이미지명에 덧붙일 drawing_style(s3에 저장시 파일명 : '현재날짜 현재시간_이미지명(drawing_style)')
# 마지막 인자로 위쪽 if문 1, 2중 어느 if문을 탔는지(if style_route , elif style_path 중 어느 if문을 탔는지)
def upload_tensor_img(bucket, tensor, img_nm, model_img_nm):
    tensor = np.array(tensor * 255, dtype=np.uint8) # normalize 해제
    image = Image.fromarray(tensor[0]) # image 화

    # 디스크에다 파일을 저장하는 것이 아닌
    # 메모리에다가 이미지를 파일 형태로 저장(잠깐 올려놓는다)
    buffer = BytesIO()
    image.save(buffer, 'PNG')
    buffer.seek(0)  # 0번째 포인터위치부터 파일을 읽으라는 뜻

    # 파일명에 붙일 현재날짜 및 시간
    current_time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    # 업로드 할 파일명
    upload_filename = f'{current_time}_{img_nm}({model_img_nm}).png'
    # MixImage app의 apps.py의 ImagedrawingstylemixConfig 클래스의 s3 객체에 해당 오브젝트를 집어넣음.
    # ACL='public-read'는 누구나 읽을 수 있도록 권한 설정.(파일이 업로드 되면서 누구나 읽을 수 있는 파일이 됨)
    # s3 에다가 업로드
    ImagedrawingstylemixConfig.s3.put_object(Bucket=bucket, Key=upload_filename, Body=buffer, ACL='public-read')
    # s3 에 올라간 파일의 링크를 리턴함
    # 하는 이유는 location에 따라서 s3 파일이 올라가는 url이 달라지기 때문.
    location = ImagedrawingstylemixConfig.s3.get_bucket_location(Bucket=bucket)['LocationConstraint']
    url = f"https://s3-{location}.amazonaws.com/{bucket}/{upload_filename}"
    return url
