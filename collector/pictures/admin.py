from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from pictures.models import ClothesPicture, ClothesPictureTag, WearingPicture, WearingPictureTag


class ClothesPictureAdmin(admin.ModelAdmin):
    list_display = ['id', 'version', 'dataset']

    def dataset(self, obj):
        return obj.get_dataset_display


class ClothesPictureTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'picture_data', 'features', 'picture_image']

    def picture_image(self, obj):
        if obj.picture:
            return mark_safe('<img src="%s" width=120px "/>' % obj.picture.url)


class WearingPictureAdmin(admin.ModelAdmin):
    list_display = ['id', 'version', 'dataset']

    def dataset(self, obj):
        return obj.get_dataset_display


class WearingPictureTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'picture_data', 'features', 'picture_image']

    def picture_image(self, obj):
        if obj.picture:
            return mark_safe('<img src="%s" width=120px "/>' % obj.picture.url)


admin.site.register(ClothesPicture, ClothesPictureAdmin)
admin.site.register(ClothesPictureTag, ClothesPictureTagAdmin)
admin.site.register(WearingPicture, WearingPictureAdmin)
admin.site.register(WearingPictureTag, WearingPictureTagAdmin)
