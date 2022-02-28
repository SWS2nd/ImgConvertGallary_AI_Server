from ninja import Schema


# 우리가 정해진 형식대로만 받아오도록 정해놓는 것이 스키마.
# 우리가 받을 형식은 파일 제목 / 이미지 파일 / 화풍용으로 섞을 이미지 파일
# 이러한 스키마 작성을 안하고 라우터에서 작성해도 되지만, 나눠서 작성하는 습관!
class ImgMixRequest(Schema):
    # 이미지명을 image_name라고 한 것.(문자열로 들어와야 한다.)
    image_name: str # str => 문자열 타입
    model_image_name: str
    # django-ninja의 경우, 스키마에서 Img를 받을 수 없기에 라우터에서 받는 것으로 함
