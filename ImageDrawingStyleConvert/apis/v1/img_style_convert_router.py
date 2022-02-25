# 원래는 import 해올때,
# from .schemas.nst_request import NstRequest
# 위와 같은 식으로 import 해왔었다면, schemas 안의 __init__.py에 작성해 놓아
# 아래와 같이 깔끔하게 import 해올 수 있다.
from .schemas import ImgCvrtResponse, ImgCvrtRequest
from ninja.files import UploadedFile
from ninja import Router, File, Form
from django.http import HttpRequest
from django.http import HttpResponse
import json
from ImageDrawingStyleConvert.services.img_style_convert_service import img_style_convert_apply


# img_style_convert_router.py에는 어떤 요청을 어떤 url로 보내면
# 어떤 함수가 실행되는지를 명시해놓는 파일

router = Router()


# ImgCvrtResponse 형태로 응답을 보낼 것이라고 명시, 이 조건에 맞지 않다면,
# 응답이 가지 않는다.
# ImgCvrtRequest: ImgCvrtRequest = Form(...)은 제목을 받을 때, ImgCvrtRequest 형식으로, Form 형태로 받겠다는 뜻.
# img: UploadedFile = File(...)은 이미지를 받을 때, UploadedFile 형식으로, File 형태로 받겠다는 뜻.
# -> dict 는 해당 함수의 return 결과 데이터타입은 dict 형식이라는 뜻.
# 결론 : 사용자는 파일 제목, 이미지 파일을 넘겨줌.
@router.post("/", response=ImgCvrtResponse)
def img_convert(request: HttpRequest, cvrt_request: ImgCvrtRequest = Form(...), image: UploadedFile = File(...)) -> HttpResponse:
    # 이미지 변환 적용 및 s3 업로드 후, url을 return 해주는 서비스 함수
    # cvrt_request.image_name엔 이미지명, img엔 이미지 파일이 있으며, 이를 인자로 넘겨줌
    file_url = img_style_convert_apply(cvrt_request.image_name, cvrt_request.model_type, image)
    print(file_url)

    # QuerySet 타입을 json으로 넘길 수 있도록 안의 값을 빼서 리스트화.
    context = {'stylized_image_url': file_url}
    return HttpResponse(json.dumps(context), content_type='application/json')
