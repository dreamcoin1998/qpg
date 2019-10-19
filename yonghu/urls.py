from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^yonghu_info/$', views.Yonghu_info),
    url(r'^yonghu_create/$', views.yonghu_create),
    url(r'^change_nickname/$', views.change_nickname)
]