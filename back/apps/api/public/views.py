import logging
import rest_framework_filters as filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import (
    NewsListSerializer,
    RetrieveDetailSerializer
)
from apps.news.models import News

logger = logging.getLogger('django.request')


class NewsFilter(filters.FilterSet):
    created__gte = filters.DateTimeFilter(name='created', lookup_expr='gte')
    created__lte = filters.DateTimeFilter(name='created', lookup_expr='lte')

    class Meta:
        model = News
        fields = [
            'created__gte',
            'created__lte',
        ]


class NewsViewSet(ReadOnlyModelViewSet):
    permission_classes = []
    authentication_classes = []

    queryset = News.objects.all()
    serializer_class_map = {
        'list': NewsListSerializer,
        'retrieve': RetrieveDetailSerializer,
    }

    filter_class = NewsFilter
    ordering_fields = ['rank__identifier']

    def get_serializer_class(self):
        serializer_class = self.serializer_class_map.get(self.action, None)
        return serializer_class or self.serializer_class
