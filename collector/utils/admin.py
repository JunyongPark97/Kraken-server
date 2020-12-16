from django.contrib import admin

# Register your models here.
from utils.features import SizeFeatures, ClothesFeatures, WearingFeatures
from utils.models import DataVersion


class DataVersionAdmin(admin.ModelAdmin):
    list_display = ['version', 'description', 'is_active']


class SizeFeaturesAdmin(admin.ModelAdmin):
    list_display = ['kind_of', 'order', 'name', 'is_active']
    list_editable = ['is_active']

    def kind_of(self, obj):
        return obj.get_kind_of_display


class ClothesFeaturesAdmin(admin.ModelAdmin):
    list_display = ['kind_of', 'order', 'name', 'is_active']
    list_editable = ['is_active']


class WearingFeaturesAdmin(admin.ModelAdmin):
    list_display = ['kind_of', 'order', 'name', 'is_active']
    list_editable = ['is_active']


admin.site.register(DataVersion, DataVersionAdmin)
admin.site.register(SizeFeatures, SizeFeaturesAdmin)
admin.site.register(ClothesFeatures, ClothesFeaturesAdmin)
admin.site.register(WearingFeatures, WearingFeaturesAdmin)
