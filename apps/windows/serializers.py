from rest_framework import serializers
from .models import *


class WindowsStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowsStat
        fields = '__all__'


class WindowsStatHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowsStatHis
        fields = '__all__'
