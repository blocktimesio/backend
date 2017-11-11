import logging

from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet
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


class RankConfigView(APIView):
    model = RankConfig
    permission_classes = [IsSuperuser]

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
