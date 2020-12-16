from django.db import models


#### PictureFeatures ####
# 1~100 : main features
# 1xx ~ : detail features
from datasets.models import KindOf

FRONT = 1
FRONT_RIGHT = 101
FRONT_LEFT = 102
REAR = 2
REAR_RIGHT = 201
REAR_LEFT = 202

##### PictureFeaturesEND #####


##### SizeFeatures #####

# Short Sleeve Size
TOTAL_LENGTH = 1
CROSS_CHEST_SECTION = 2
CROSS_BOTTOM_SECTION = 3
SLEEVE_LENGTH = 4
SHOULDER_LENGTH = 5
SLEEVE_CROSS_SECTION = 6
NECK_CROSS_SECTION = 7

Short_Sleeve_Size_Features = (
        (TOTAL_LENGTH, '총장'),
        (CROSS_CHEST_SECTION, '가슴단면'),
        (CROSS_BOTTOM_SECTION, '밑단면'),
        (SLEEVE_LENGTH, '소매길이'),
        (SHOULDER_LENGTH, '어꺠길이'),
        (SLEEVE_CROSS_SECTION, '소매단면'),
        (NECK_CROSS_SECTION, '목단면'),
    )

##### SizeFeaturesEND #####


class SizeFeatures(models.Model):
    kind_of = models.ForeignKey(KindOf, on_delete=models.PROTECT, related_name='size_features')
    name = models.CharField(max_length=200, help_text='특징의 이름입니다')
    order = models.PositiveIntegerField(help_text='데이터 기입 순서에 사용합니다.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '[{}] {}'.format(self.kind_of.kinds, self.name)

    class Meta:
        verbose_name = '사이즈 데이터 feature'
        verbose_name_plural = '사이즈 데이터 features'


class ClothesFeatures(models.Model):
    kind_of = models.ForeignKey(KindOf, on_delete=models.PROTECT, related_name='clothes_features')
    name = models.CharField(max_length=200, help_text='특징의 이름입니다')
    order = models.PositiveIntegerField(help_text='사진 촬영 순서에 사용합니다.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '[{}] {}'.format(self.kind_of.kinds, self.name)

    class Meta:
        verbose_name = '옷 사진 데이터 feature'
        verbose_name_plural = '옷 사진 데이터 features'


class WearingFeatures(models.Model):
    kind_of = models.ForeignKey(KindOf, on_delete=models.PROTECT, related_name='wearing_features')
    name = models.CharField(max_length=200, help_text='특징의 이름입니다')
    order = models.PositiveIntegerField(help_text='사진 촬영 순서에 사용합니다.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '[{}] {}'.format(self.kind_of.kinds, self.name)

    class Meta:
        verbose_name = '옷 입은 사진 데이터 feature'
        verbose_name_plural = '옷 입은 사진 데이터 features'
