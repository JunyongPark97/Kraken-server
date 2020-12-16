from django.db import models

from utils.tools import random_name_generator


class KindOf(models.Model):
    """
    Dataset 의 종류입니다.
    Dataset model , 각각의 features model 과 1:N 관계입니다.
    """
    kinds = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.kinds)

    class Meta:
        verbose_name = '데이터 종류'
        verbose_name_plural = '데이터 종류'


class Dataset(models.Model):
    """
    데이터 메인 모델
    size, clothes(picture), wearing(pictures) 와 1:N / 버전관리를 위해 1:N 으로 선언하였습니다.

    ## Size queryset ex [from Size object]
    size_data = SizeOfShortSleeve.objects.filter(short_sleeve__name='test', version=1).last()
    ## Size queryset ex [from Dataset object]
    size_data = ShortSleeve.objects.get(name='test').sizes
    """
    kind_of = models.ForeignKey(KindOf, on_delete=models.PROTECT, related_name='dataset')
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    old_name = models.CharField(max_length=50, null=True, blank=True, help_text='서버 만들기 전 참고가위해 만든 이름들')
    old_file_name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return '[{}] {}'.format(self.kind_of.kinds, self.name)

    class Meta:
        verbose_name = '데이터셋'
        verbose_name_plural = '데이터셋'

    def save(self, *args, **kwargs):
        self.name = random_name_generator(8)
        super(Dataset, self).save(*args, **kwargs)


class RemarkTag(models.Model):
    """
    각 옷에대한 특징을 기록합니다
    ex: 재질, 늘어남, 색상 등
    """
    color = models.CharField(max_length=30, null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    spread = models.BooleanField(null=True)
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE)
