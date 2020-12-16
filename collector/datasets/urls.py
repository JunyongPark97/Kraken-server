from django.urls import path, include
from rest_framework.routers import SimpleRouter

from datasets.views import ShortSleeveSizeUploadManageTemplateView, StaffManageTemplateView, \
    ShortSleeveCheckNRedirectView, ShortSleeveClothesPictureUploadTemplateView, \
    ShortSleeveWearingPictureUploadTemplateView

urlpatterns = [
    path('', StaffManageTemplateView.as_view(), name='home'),
    path('check/short_sleeve/', ShortSleeveCheckNRedirectView.as_view(), name='check_short_sleeve'),
    path('short-sleeve/<int:pk>/size/', ShortSleeveSizeUploadManageTemplateView.as_view(), name='short_sleeve_size_upload'),
    path('short-sleeve/<int:pk>/clothes-picture/',
         ShortSleeveClothesPictureUploadTemplateView.as_view(),
         name='short_sleeve_clothes_picture_upload'),
    path('short-sleeve/<int:pk>/wearing-picture/',
         ShortSleeveWearingPictureUploadTemplateView.as_view(),
         name='short_sleeve_wearing_picture_upload'),
]