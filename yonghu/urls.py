from django.conf.urls import url
from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter
from .views import YonghuInfo, UpdataPassword


# yonghu_update = YonghuInfo.as_view({
#     'post': 'update'
# })


router = DefaultRouter()
router.register('yonghu_info', YonghuInfo, base_name='yonghu_info')
router.register('update_password', UpdataPassword, base_name='updata_password')


urlpatterns = [
    url(r'^yonghu_create/$', views.yonghu_create),
    url(r'^activate/$', views.active_email),
    url(r'^test_email/$', views.email_test),
    url(r'^yonghu_login/$', views.yonghu_login),
    path('email_code/', views.email_code),
    path('email_login/', views.email_login),
    path('find_passwd_by_email/', views.FindPasswordByEmail.as_view()),
] + router.urls