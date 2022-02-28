from ninja import Schema


# 전달해 주는 대답은 s3에 올라간 변환된 이미지의 url을 전달!
class ImgMixResponse(Schema):
    mixed_img_url: str
    check: int
