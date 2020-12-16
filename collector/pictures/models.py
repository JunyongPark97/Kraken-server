from io import BytesIO

from PIL import ExifTags
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from datasets.models import Dataset
from utils.features import ClothesFeatures, WearingFeatures
from utils.models import DataVersion

from utils.tools import random_name_generator


def get_random_image_name(picture_data):
    ext = 'jpeg'
    key = random_name_generator(6)
    filename = "%s_%s.%s" % (picture_data.dataset.name, key, ext)
    return filename


def img_directory_path_clothes_picture(instance, filename):
    ext = filename.split('.')[-1]
    key = random_name_generator(6)
    filename = "%s_%s.%s" % (instance.picture_data.dataset.name, key, ext)
    return 'picture/clothes/{}/{}/{}'.\
        format(instance.features.kind_of.kinds, instance.picture_data.version.version, filename)


def img_directory_path_wearing_picture(instance, filename):
    ext = filename.split('.')[-1]
    key = random_name_generator(6)
    filename = "%s_%s.%s" % (instance.picture_data.dataset.name, key, ext)
    return 'picture/wearing/{}/{}/{}'. \
        format(instance.features.kind_of.kinds, instance.picture_data.version.version, filename)


class ClothesPicture(models.Model):
    """
    데이터 옷 사진
    tags 에서 각 특징에 대해 관리합니다.
    이 모델과 Dataset 모델은 버전관리를 위해 N:1 관계입니다.
    """
    version = models.ForeignKey(DataVersion, on_delete=models.CASCADE, related_name='clothes_pictures')
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='clothes_pictures')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return '[{}] name:{}'.format(self.version, self.dataset.name)

    class Meta:
        verbose_name = '옷 사진 데이터'
        verbose_name_plural = '옷 사진 데이터'


class ClothesPictureTag(models.Model):
    """
    데이터 옷 사진 tag
    실제 이미지가 저장되는 모델
    features 에 하나의 옷 사진이 생성됩니다.
    """
    picture_data = models.ForeignKey(ClothesPicture, on_delete=models.CASCADE, related_name='tags')
    features = models.ForeignKey(ClothesFeatures, on_delete=models.CASCADE, related_name='clothes_picture_tags')
    picture = models.ImageField(upload_to=img_directory_path_clothes_picture)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '옷 사진 데이터 Tag'
        verbose_name_plural = '옷 사진 데이터 Tag'

    @property
    def image_url(self):
        return self.picture.url


class WearingPicture(models.Model):
    """
    데이터 옷 착용 사진
    tags 에서 각 특징에 대해 관리합니다.
    이 모델과 dataset 의 ShortSleeve 모델은 버전관리를 위해 N:1 관계입니다.
    """
    version = models.ForeignKey(DataVersion, on_delete=models.CASCADE, related_name='wearing_pictures')
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='wearing_pictures')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '옷 입은 사진 데이터'
        verbose_name_plural = '옷 입은 사진 데이터'


class WearingPictureTag(models.Model):
    """
    데이터 옷 착용 사진 tag
    실제 이미지가 저장되는 모델
    features 에 하나의 옷 사진이 생성됩니다.
    """
    picture_data = models.ForeignKey(WearingPicture, on_delete=models.CASCADE, related_name='tags')
    features = models.ForeignKey(WearingFeatures, on_delete=models.CASCADE, related_name='wearing_picture_tags')
    picture = models.ImageField(upload_to=img_directory_path_wearing_picture)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '옷 입은 사진 데이터 Tag'
        verbose_name_plural = '옷 입은 사진 데이터 Tag'
