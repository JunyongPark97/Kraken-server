from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from pictures.models import ClothesPicture, ClothesPictureTag
from sizes.models import Size, SizeTag


class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'version', 'dataset']

    def dataset(self, obj):
        return obj.get_dataset_display


class SizeTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'size_data', 'features', 'value']


admin.site.register(Size, SizeAdmin)
admin.site.register(SizeTag, SizeTagAdmin)