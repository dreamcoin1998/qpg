from django.conf.urls import url
from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter
from .views import YonghuInfo


# yonghu_update = YonghuInfo.as_view({
#     'post': 'update'
# })


router = DefaultRouter()
router.register('yonghu_info', YonghuInfo, base_name='yonghu_info')


urlpatterns = [
    url(r'^yonghu_create/$', views.yonghu_create),
    url(r'^activate/$', views.active_email),
    url(r'^test_email/$', views.email_test),
    url(r'^yonghu_login/$', views.yonghu_login),
    url(r'^aaaa/$', views.Yonghu_info),
] + router.urls