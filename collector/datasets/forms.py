from django import forms

from datasets.models import KindOf, Dataset
from pictures.models import ClothesPictureTag, WearingPictureTag
from sizes.models import Size, SizeTag
from utils.features import SizeFeatures, ClothesFeatures, WearingFeatures
from utils.models import DataVersion
from fractions import Fraction


class ShortSleeveSizeUploadForm(forms.ModelForm):
    kinds = KindOf.objects.get(kinds='short_sleeve')

    def __init__(self, *args, **kwargs):
        super(ShortSleeveSizeUploadForm, self).__init__(*args, **kwargs)
        for feature in SizeFeatures.objects.filter(kind_of=self.kinds, is_active=True):
            self.fields[feature.name] = forms.FloatField()

    class Meta:
        model = SizeTag
        fields = []


class ShortSleeveClothesPictureUploadForm(forms.ModelForm):
    kinds = KindOf.objects.get(kinds='short_sleeve')

    def __init__(self, *args, **kwargs):
        super(ShortSleeveClothesPictureUploadForm, self).__init__(*args, **kwargs)
        features = ClothesFeatures.objects.filter(kind_of=self.kinds, is_active=True).order_by('order')
        for feature in features:
            self.fields[feature.name] = \
                forms.FileField(widget=forms.ClearableFileInput(attrs={
                    'type':'file',
                    'accept':'image/*',
                    'capture':'camera'
                }))

    class Meta:
        model = ClothesPictureTag
        fields = []


class ShortSleeveWearingPictureUploadForm(forms.ModelForm):
    kinds = KindOf.objects.get(kinds='short_sleeve')

    def __init__(self, *args, **kwargs):
        super(ShortSleeveWearingPictureUploadForm, self).__init__(*args, **kwargs)
        features = WearingFeatures.objects.filter(kind_of=self.kinds, is_active=True).order_by('order')
        for feature in features:
            self.fields[feature.name] = \
                forms.FileField(widget=forms.ClearableFileInput(attrs={
                    'type':'file',
                    'accept':'image/*',
                    'capture':'camera'
                }))

    class Meta:
        model = WearingPictureTag
        fields = []
