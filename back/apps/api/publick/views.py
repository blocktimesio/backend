import logging
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import (
    NewsListSerializer, NewsDetailSerializer
)
from apps.news.models import (Tag, Domain, News, RankConfig)

logger = logging.getLogger('django.request')


class NewsViewSet(ReadOnlyModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = News.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = sorted(queryset, key=lambda n: n.rank, reverse=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NewsListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NewsListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = NewsDetailSerializer(instance)
        return Response(serializer.data)
