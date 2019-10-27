from rest_framework import routers
from django.urls import path
from . import views
from .models import Youshengshu
from .serializers import YoushengshuSerializer


urlpatterns = [
    path('info/<int:pk>', views.BookInfo.as_view()),
    path('type/<str:type>', views.BookTypeList.as_view()),
    path('voice/<str:voice>', views.BookVoiceList.as_view()),
    path('author/<str:author>', views.BookAuthorList.as_view()),
    path('sound', views.booksound),
    path('typelist', views.xmlyTypeList),
    path('search', views.xmlySearch),
    path('detail', views.xmlyAllji),
]