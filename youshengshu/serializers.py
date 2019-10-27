from rest_framework import serializers
from .models import Youshengshu


class YoushengshuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youshengshu
        fields = ('id', 'author', 'name', 'voice', 'type', 'time', 'status')