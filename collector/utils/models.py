from django.db import models


class DataVersion(models.Model):
    """
    Data 의 버전을 관리합니다.
    """
    version = models.FloatField()
    description = models.CharField(max_length=200, help_text='해당 버전의 기술적 목적을 적어주세요')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, help_text='활성화된 버전. true 인 경우 앞으로 쌓는 데이터 버전으로 설정 됨')

    def __str__(self):
        return '[version {}] {}'.format(self.version, self.description)

    def save(self, *args, **kwargs):
        if self.is_active:
            # https://stackoverflow.com/questions/1455126/unique-booleanfield-value-in-django
            try:
                temp = DataVersion.objects.get(is_active=True)
                if self != temp:
                    temp.is_active = False
                    temp.save()
            except DataVersion.DoesNotExist:
                pass
        super(DataVersion, self).save(*args, **kwargs)