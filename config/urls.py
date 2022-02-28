"""nst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from ImageDrawingStyleConvert.apis.v1.img_style_convert_router import router as cvrt_router
from MixImage.apis.v1.img_style_mix_router import router as mix_router


api = NinjaAPI()

# /api/convert -> ImageDrawingStyleConvert app 관련
api.add_router("/convert/", cvrt_router)
# /api/mix -> MixImage app 관련
api.add_router("/mix/", mix_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
