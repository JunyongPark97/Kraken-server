from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe

from datasets.models import Dataset, KindOf, RemarkTag
from pictures.models import ClothesPictureTag, WearingPictureTag
from sizes.models import SizeTag
from utils.models import DataVersion


def dictnorm(data):
    new_dict = {}
    data = list(data.values())
    new_dict[data[0]] = data[1]
    return new_dict


class DataSetsAdmin(admin.ModelAdmin):
    list_display = ['id', 'kinds', 'name', 'old_file_name', 'before_name', 'represent', 'clothes_images', 'wearing_pictures', 'sizes']
    list_per_page = 50

    def kinds(self, obj):
        return obj.kind_of.description

    def before_name(self, obj):
        if not obj.old_name:
            return '-'
        if len(obj.old_name) >= 7:
            new_string = obj.old_name[:7] + '...'
        else:
            new_string = obj.old_name
        return new_string
    before_name.short_description = '이전참고이름'

    def sizes(self, obj):
        size_data = obj.sizes.all()
        string = ''
        active_version = DataVersion.objects.filter(is_active=True).last().version
        for size in size_data:  # each version
            version = size.version.version
            values = SizeTag.objects.filter(size_data=size).values_list('value')
            temp_string = ''
            i = 1
            for value in values:
                temp_string += '{}|'.format(value[0])
                if i % 4 == 0:
                    temp_string += '</br>'
                i += 1
            string += '<h3 style="font-size: 13px;">v.{} :</br>'.format(version) + temp_string + '</h3>'
        collect_link = '<h3 style="font-size: 12px;"><a href={}>[활성 버전 v.{}] </br>Size 업로드/수정하러가기 </a></h3>'.format(
            reverse("short_sleeve_size_upload", args=(obj.pk,)), active_version)
        string = string + collect_link
        return mark_safe(string)

    def represent(self, obj):
        if not obj.clothes_pictures.exists() or not obj.clothes_pictures.first().tags.exists():
            return '-'
        versions = obj.clothes_pictures.all()
        temp = {}
        i = 0
        string = ''
        for version in versions:
            image = ClothesPictureTag.objects.filter(picture_data=version, picture_data__dataset=obj).first()
            temp[version] = image.picture.url
            string += '<h3>v.{} <img src={} width=100px "/></h3>'.format(list(temp.keys())[i].version.version, temp[list(temp.keys())[i]])
            i += 1

        return mark_safe(string)
    represent.short_description = '대표이미지'

    def clothes_images(self, obj):
        # if not obj.clothes_pictures.exists():
        #     return 'go to work' # page link with id => /{}id/
        kind_of = obj.kind_of
        number_of_features = kind_of.clothes_features.filter(is_active=True).count()
        versions = obj.clothes_pictures.all()
        string = ''
        active_version = DataVersion.objects.filter(is_active=True).last().version
        for version in versions:
            num_of_clothes_pictures = ClothesPictureTag.objects.filter(picture_data=version, picture_data__dataset=obj).count()
            string += '<h3 style="font-size: 13px; color: blue;">v.{} : {}/{}</h3>'.format(version.version.version, num_of_clothes_pictures, number_of_features)
        collect_link = '<h3 style="font-size: 12px;"><a href={}>[활성 버전 v.{}] </br>옷 Image 업로드/수정하러가기 </a></h3>'.format(
                    reverse("short_sleeve_clothes_picture_upload", args=(obj.pk,)), active_version)
        string = string + collect_link
        return mark_safe(string)
    clothes_images.short_description = '|사진 업로드'

    def wearing_pictures(self, obj):
        kind_of = obj.kind_of
        number_of_features = kind_of.wearing_features.filter(is_active=True).count()
        versions = obj.wearing_pictures.all()
        string = ''
        active_version = DataVersion.objects.filter(is_active=True).last().version
        for version in versions:
            num_of_wearing_pictures = WearingPictureTag.objects.filter(picture_data=version,
                                                                       picture_data__dataset=obj).count()
            string += '<h3 style="font-size: 13px;  color: brown;">v.{} : {}/{}</h3>'.format(version.version.version,
                                                                              num_of_wearing_pictures,
                                                                              number_of_features)
        collect_link = '<h3 style="font-size: 12px;"><a href={}>[활성 버전 v.{}] </br>사람 Image 업로드/수정하러가기 </a></h3>'.format(
            reverse("short_sleeve_wearing_picture_upload", args=(obj.pk,)), active_version)
        string = string + collect_link
        return mark_safe(string)

    wearing_pictures.short_description = '입은 사진 업로드'


class KindOfAdmin(admin.ModelAdmin):
    list_display = ['kinds', 'description', 'created_at', 'is_active']


class RemarkTagAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'color', 'material', 'spread']


admin.site.register(Dataset, DataSetsAdmin)
admin.site.register(KindOf, KindOfAdmin)
admin.site.register(RemarkTag, RemarkTagAdmin)