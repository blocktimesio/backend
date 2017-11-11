import logging

from bson import ObjectId
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework_mongoengine.generics import get_object_or_404
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet, GenericViewSet
from apps.api.permissions import IsSuperuser
from .serializers import (NewsSerializer, RankConfigSerializer, SignInSerializer)
from apps.news.models import (News, RankConfig)
from django.contrib.auth import (
    login as django_login,
    authenticate)

logger = logging.getLogger('django.request')


class NewsViewSet(MongoModelViewSet):
    lookup_field = 'id'
    serializer_class = NewsSerializer

    def get_queryset(self):
        return sorted(News.objects.all(), key=lambda n: n.rank, reverse=True)

    def get_object(self):
        queryset = self.filter_queryset(News.objects.all())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        if 'id' in filter_kwargs:
            filter_kwargs['id'] = ObjectId(filter_kwargs['id'])
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


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
