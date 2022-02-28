# 원래는 import 해올때,
# from .schemas.nst_request import NstRequest
# 위와 같은 식으로 import 해왔었다면, schemas 안의 __init__.py에 작성해 놓아
# 아래와 같이 좀 더 깔끔하게 import 해올 수 있다.
from .schemas import ImgMixRequest,ImgMixResponse
from ninja.files import UploadedFile
from ninja import Router, File, Form
from django.http import HttpRequest
from django.http import HttpResponse
import json
from MixImage.services.img_style_mix_service import img_style_mix_apply


router = Router()


# ImgMixResponse 형태로 응답을 보낼 것이라고 명시, 이 조건에 맞지 않다면,
# 응답이 가지 않는다.
# ImgMixRequest: ImgMixRequest = Form(...)은 제목을 받을 때, ImgMixRequest 형식으로, Form 형태로 받겠다는 뜻.
# image: UploadedFile = File(...)은 이미지를 받을 때, UploadedFile 형식으로, File 형태로 받겠다는 뜻.
# -> HttpResponse 는 해당 함수의 return 결과 데이터타입은 HttpResponse 형식이라는 뜻.
# 결론 : 사용자는 파일 제목, 이미지 파일을 넘겨줌.
@router.post("/", response=ImgMixResponse)
def img_mix(request: HttpRequest,
            mix_request: ImgMixRequest = Form(...),
            image: UploadedFile = File(...),
            model_image: UploadedFile = File(...)) -> HttpResponse:
    # 이미지 변환 적용 및 s3 업로드 후, url을 return 해주는 서비스 함수
    # mix_request.image_name엔 이미지명, mix_request.model_image_name엔 모델 이미지명,
    # image, model_image엔 이미지 파일이 있으며, 이를 인자로 넘겨줌
    file_url = img_style_mix_apply(mix_request.image_name, mix_request.model_image_name,
                                   image, model_image)
    print(request)
    print(file_url)

    context = {'mixed_img_url': file_url, 'check': 1}
    return HttpResponse(json.dumps(context), content_type='application/json')
