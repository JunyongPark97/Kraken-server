from django.db import models

from datasets.models import Dataset
from utils.features import SizeFeatures
from utils.models import DataVersion


class Size(models.Model):
    """
    사이즈 모델
    version 으로 관리 (1차, 2차 ..)
    tags 로 features / value 관리
    """
    version = models.ForeignKey(DataVersion, on_delete=models.CASCADE, related_name='sizes') # 임시 CASCADE
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='sizes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SizeTag(models.Model):
    """
    반팔 각 특징에 대한 사이즈입니다.
    tag 의 개념으로 사용합니다.
    """
    size_data = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='tags')
    features = models.ForeignKey(SizeFeatures, on_delete=models.CASCADE, related_name='sizes') # 임시 CASCADE
    value = models.FloatField(help_text='단위 cm / 잴 수 없으면 -1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)











