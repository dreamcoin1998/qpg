from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('auth/', include('yonghu.urls')),
]