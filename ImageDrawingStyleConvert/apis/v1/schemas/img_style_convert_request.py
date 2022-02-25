from ninja import Schema


# 우리가 정해진 형식대로만 받아오도록 정해놓는 것이 스키마.
# 우리가 받을 형식은 파일 제목 / 이미지 파일 그 자체
# 이러한 스키마 작성을 안하고 라우터에서 작성해도 되지만, 나눠서 작성하는 습관!
class ImgCvrtRequest(Schema):
    # 이미지명을 img_nm라고 한 것.(문자열로 들어와야 한다.)
    image_name: str # str => 문자열 타입
    model_type: str
    # 장고 닌자의 경우 하나의 스키마 안에서 파일도 받을 수 있도록 하지 않기에 아래는 패스
    # img: UploadFile # 이 부분은 장고 닌자를 사용함으로 따로 라우터에서 작성하겠다.
