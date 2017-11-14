import os
import logging
from django.conf import settings
import rest_framework_filters as filters
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.viewsets import (ModelViewSet, ReadOnlyModelViewSet)
from .serializers import (
    DomainSerializer, TagSerializer, NewsSerializer,
    RankConfigSerializer, SignInSerializer
)
from apps.news.models import (Tag, Domain, News, RankConfig)
from django.contrib.auth import (
    authenticate,
    login as django_login
)

logger = logging.getLogger('django.request')


class DomainViewSet(ReadOnlyModelViewSet):
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class DomainFilter(filters.FilterSet):

    class Meta:
        model = Domain
        fields = {
            'name': ['exact'],
            'id': ['exact', 'in'],
        }


class NewsFilter(filters.FilterSet):
    domain = filters.RelatedFilter(DomainFilter, name='domain', queryset=Domain.objects.all())

    class Meta:
        model = News
        fields = {'domain': ['exact', 'in']}


class NewsViewSet(ModelViewSet):
    filter_class = NewsFilter
    serializer_class = NewsSerializer
    queryset = News.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = sorted(queryset, key=lambda n: n.rank, reverse=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RankConfigView(APIView):
    model = RankConfig
    permission_classes = []

    def get(self, request, format=None):
        obj = self.model.get_solo()
        serializer = RankConfigSerializer(instance=obj)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RankConfigSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        try:
            self.model.objects.update(**serializer.data)
        except Exception as e:
            message = 'Error at saving RankConfig'
            logger.error(message, exc_info=True)
            raise APIException(message)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def patch(self, request, format=None):
        return self.post(request, format)


class SignInView(APIView):
    def post(self, request, format=None):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, **serializer.data)
            if user:
                django_login(request, user, settings.AUTHENTICATION_BACKENDS)
                data = dict(sessionid=request.session.session_key)
                return Response(data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        return self.post(request, format)


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def load_image(request):
    if request.method == 'POST':
        image_path = 'news_images/{}'.format(request.FILES['file'].name)
        content = request.FILES['file'].file.read()
        uploaded_path = default_storage.save(image_path, ContentFile(content))
        link = os.path.join(settings.MEDIA_URL, uploaded_path)
        return JsonResponse({'link': link})
    return JsonResponse({})
