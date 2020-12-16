from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import routers, serializers, viewsets
from django.views.generic import DetailView, TemplateView
from rest_framework.decorators import action
from rest_framework.views import APIView
from PIL import Image
from PIL import ExifTags
from io import BytesIO
from datasets.forms import ShortSleeveSizeUploadForm, ShortSleeveClothesPictureUploadForm, \
    ShortSleeveWearingPictureUploadForm
from datasets.models import Dataset, KindOf
from pictures.models import ClothesPicture, ClothesPictureTag, WearingPicture, WearingPictureTag
from sizes.models import Size, SizeTag
from utils.features import ClothesFeatures, SizeFeatures, WearingFeatures
from utils.models import DataVersion
from utils.tools import ratate_image


class StaffManageTemplateView(TemplateView):
    """
    Staff Management Page
    """
    template_name = 'start_page.html'

    def get_context_data(self, **kwargs):
        context = super(StaffManageTemplateView, self).get_context_data()
        context['user'] = self.request.user
        # context['crawl_fails'] = ProductCrawlFailedUploadRequest.objects.filter(is_done=False)
        context['short_sleeve_pk'] = self.get_short_sleeve_pk()
        return context

    def get_short_sleeve_pk(self):
        if Dataset.objects.filter(clothes_pictures__isnull=True).exists():
            dataset = Dataset.objects.filter(clothes_pictures__isnull=True).first()
        else:
            kinds = KindOf.objects.get(kinds='short_sleeve')
            dataset = Dataset.objects.create(kind_of=kinds)
        return dataset.pk


class ShortSleeveCheckNRedirectView(APIView): # TODO : use ViewSet, Router / reverse url 때문에 안썼음

    def get(self, request, pk=None):
        delete_qs = Dataset.objects.filter(clothes_pictures__isnull=True, wearing_pictures__isnull=True)
        if delete_qs.exists():
            delete_qs = delete_qs.filter(Q(sizes__tags__isnull=True)|Q(sizes__isnull=True))
            delete_qs.delete()

        # print('===')
        # if Size.objects.filter(tags__isnull=True).exists():
        #     print('asdasd')
        #     size = Size.objects.filter(sizes__isnull=True).last()
        # else:
        #     print('=wdwd')
        #     dataset = Dataset.objects.create(kind_of=KindOf.objects.get(kinds='short_sleeve'))
        # print(dataset.pk)
        #
        # size, _ = Size.objects.get_or_create(version=DataVersion.objects.filter(is_active=True).last(), dataset=dataset)
        # return redirect('short_sleeve_size_upload', size.pk)


class ShortSleeveClothesPictureUploadTemplateView(DetailView):
    template_name = 'clothes_picture_upload_page.html'
    kinds = KindOf.objects.get(kinds='short_sleeve')
    queryset = Dataset.objects.filter(kind_of=kinds)

    def get_context_data(self, **kwargs):
        context = super(ShortSleeveClothesPictureUploadTemplateView, self).get_context_data()
        form = ShortSleeveClothesPictureUploadForm
        name = self.get_object().name
        version = DataVersion.objects.filter(is_active=True).last()
        context['form'] = form
        context['name'] = name
        context['version'] = version
        context['other_queryset'] = self.get_other_version_qs()
        return context

    def get_other_version_qs(self):
        version = DataVersion.objects.filter(is_active=True).last()
        queryset = self.get_object().clothes_pictures.exclude(version=version)
        return queryset

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = ShortSleeveClothesPictureUploadForm(request.POST, request.FILES)
        pk = self.kwargs.get(self.pk_url_kwarg)
        if form.is_valid():
            version = DataVersion.objects.filter(is_active=True).last()
            self._get_features_queryset()
            dataset = self.get_queryset().filter(pk=pk).last()

            # 같은 버전 이전 사진 데이터 삭제
            dataset.clothes_pictures.filter(version=version).delete()

            # 버전은 admin 에서 active로 관리
            picture_data = ClothesPicture.objects.create(version=version, dataset=dataset)

            for field in form.cleaned_data:
                feature = self.features.filter(name=field).first()

                tmp = form.cleaned_data[field]
                byteImg = Image.open(tmp)

                rotated_image = ratate_image(byteImg)

                byteIO = BytesIO()
                rotated_image.save(byteIO, "JPEG")
                byteIO.seek(0)
                picture = InMemoryUploadedFile(byteIO, None, 'picture.jpg', 'image/jpeg', len(byteIO.getvalue()), None)

                ClothesPictureTag.objects.create(picture_data=picture_data, features=feature, picture=picture)

            # 새로운 dataset 생성, 이전에 생성된 dataset이 존재한다면 사용.
            if Dataset.objects.filter(clothes_pictures__isnull=True).exists():
                new_dataset = Dataset.objects.filter(clothes_pictures__isnull=True).first()
            else:
                new_dataset = Dataset.objects.create(kind_of=self.kinds)
            return redirect('short_sleeve_clothes_picture_upload', new_dataset.pk)

        return redirect('short_sleeve_clothes_picture_upload', pk)

    def _get_features_queryset(self):
        self.kinds = KindOf.objects.get(kinds='short_sleeve')
        self.features = ClothesFeatures.objects.filter(kind_of=self.kinds, is_active=True).order_by('order')


# Wearing
class ShortSleeveWearingPictureUploadTemplateView(DetailView):
    template_name = 'wearing_picture_upload_page.html'
    kinds = KindOf.objects.get(kinds='short_sleeve')
    queryset = Dataset.objects.filter(kind_of=kinds).filter(clothes_pictures__isnull=False).distinct()

    def get_context_data(self, **kwargs):
        context = super(ShortSleeveWearingPictureUploadTemplateView, self).get_context_data()
        version = DataVersion.objects.filter(is_active=True).last()

        context['form'] = ShortSleeveWearingPictureUploadForm
        context['name'] = self.get_object().name
        context['version'] = version
        context['prev'] = self.has_prev()
        context['next'] = self.has_next()
        context['other_queryset'] = self.get_other_version_qs()
        context['represent_image'] = self.get_represent_image()
        return context

    def get_other_version_qs(self):
        version = DataVersion.objects.filter(is_active=True).last()
        queryset = self.get_object().wearing_pictures.exclude(version=version)
        return queryset

    def get_represent_image(self):
        image = ClothesPictureTag.objects.filter(picture_data__dataset=self.get_object()).first()
        return image

    def has_prev(self):
        pk = self.kwargs['pk']
        prev_obj = self.get_queryset().filter(pk__lt=pk).order_by('pk').last()
        return prev_obj

    def has_next(self):
        pk = self.kwargs['pk']
        next_obj = self.get_queryset().filter(pk__gt=pk).order_by('pk').first()
        return next_obj

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = ShortSleeveWearingPictureUploadForm(request.POST, request.FILES)
        pk = self.kwargs.get(self.pk_url_kwarg)
        if form.is_valid():
            version = DataVersion.objects.filter(is_active=True).last()
            self._get_features_queryset()
            dataset = self.get_queryset().filter(pk=pk).last()

            # 같은 버전 이전 사진 데이터 삭제
            dataset.wearing_pictures.filter(version=version).delete()

            # 버전은 admin 에서 active로 관리
            picture_data = WearingPicture.objects.create(version=version, dataset=dataset)

            for field in form.cleaned_data:
                feature = self.features.filter(name=field).first()

                tmp = form.cleaned_data[field]
                byteImg = Image.open(tmp)

                rotated_image = ratate_image(byteImg)

                byteIO = BytesIO()
                rotated_image.save(byteIO, "JPEG")
                byteIO.seek(0)
                picture = InMemoryUploadedFile(byteIO, None, 'picture.jpg', 'image/jpeg', len(byteIO.getvalue()), None)

                WearingPictureTag.objects.create(picture_data=picture_data, features=feature, picture=picture)

            if self.has_next():
                pk = self.has_next().pk
                return redirect('short_sleeve_wearing_picture_upload', pk)
            else:
                return redirect('admin:index')

        return redirect('short_sleeve_wearing_picture_upload', pk)

    def _get_features_queryset(self):
        self.kinds = KindOf.objects.get(kinds='short_sleeve')
        self.features = WearingFeatures.objects.filter(kind_of=self.kinds, is_active=True).order_by('order')


# Size
class ShortSleeveSizeUploadManageTemplateView(DetailView):
    template_name = 'size_upload_page.html'
    permission_classes = ['IsAuthenticated', ]
    kinds = KindOf.objects.get(kinds='short_sleeve')
    queryset = Dataset.objects.filter(kind_of=kinds).filter(clothes_pictures__isnull=False).distinct()

    def get_context_data(self, **kwargs):
        context = super(ShortSleeveSizeUploadManageTemplateView, self).get_context_data()
        form = ShortSleeveSizeUploadForm
        name = self.get_object().name
        version = DataVersion.objects.filter(is_active=True).last()

        context['form'] = form
        context['name'] = name
        context['version'] = version
        context['prev'] = self.has_prev()
        context['next'] = self.has_next()
        context['queryset'] = self.get_version_qs()
        context['represent_image'] = self.get_represent_image()
        return context

    def get_version_qs(self):
        queryset = self.get_object().sizes.all()
        return queryset

    def get_represent_image(self):
        image = ClothesPictureTag.objects.filter(picture_data__dataset=self.get_object()).first()
        return image

    def has_prev(self):
        pk = self.kwargs['pk']
        prev_obj = self.get_queryset().filter(pk__lt=pk).order_by('pk').last()
        return prev_obj

    def has_next(self):
        pk = self.kwargs['pk']
        next_obj = self.get_queryset().filter(pk__gt=pk).order_by('pk').first()

        return next_obj

    def _get_features_queryset(self):
        self.kinds = KindOf.objects.get(kinds='short_sleeve')
        self.features = SizeFeatures.objects.filter(kind_of=self.kinds, is_active=True).order_by('order')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = ShortSleeveSizeUploadForm(data=request.POST)
        bulk_list = []
        pk = self.kwargs.get(self.pk_url_kwarg)
        if form.is_valid():
            version = DataVersion.objects.filter(is_active=True).last()

            self._get_features_queryset()

            # 같은 버전 이전 사진 데이터 삭제
            self.get_object().sizes.filter(version=version).delete()

            # 버전은 admin 에서 active로 관리
            size_data, _ = Size.objects.get_or_create(version=version, dataset=self.get_object())

            for field in form.cleaned_data:
                feature = self.features.filter(name=field).first()
                bulk_list.append(SizeTag(
                    size_data=size_data,
                    features=feature,
                    value=form.cleaned_data[field]
                ))
            SizeTag.objects.bulk_create(bulk_list)
            if self.has_next():
                pk = self.has_next().pk
            else:
                pk = self.kwargs.get(self.pk_url_kwarg)
            return redirect('short_sleeve_size_upload', pk)

        return redirect('short_sleeve_size_upload', pk)
