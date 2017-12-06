import logging
import rest_framework_filters as filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import (
    NewsListSerializer,
    NewsRetrieveDetailSerializer,
    PostListSerializer,
    PostRetrieveDetailSerializer,
    FlatpageSerializer
)
from apps.news.models import News
from apps.post.models import Post
from apps.flatpage.models import Flatpage

logger = logging.getLogger('django.request')


class SerializerViewMixin(object):
    serializer_class = None
    serializer_class_map = {}

    def get_serializer_class(self):
        serializer_class = self.serializer_class_map.get(self.action, None)
        return serializer_class or self.serializer_class


class AccessViewMixin(object):
    permission_classes = []
    authentication_classes = []


class NewsFilter(filters.FilterSet):
    created__gte = filters.DateTimeFilter(name='created', lookup_expr='gte')
    created__lte = filters.DateTimeFilter(name='created', lookup_expr='lte')

    class Meta:
        model = News
        fields = [
            'created__gte',
            'created__lte',
        ]


class NewsViewSet(SerializerViewMixin, AccessViewMixin, ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class_map = {
        'list': NewsListSerializer,
        'retrieve': NewsRetrieveDetailSerializer,
    }
    filter_class = NewsFilter
    ordering_fields = ['rank__identifier']


class PostViewSet(SerializerViewMixin, AccessViewMixin, ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class_map = {
        'list': PostListSerializer,
        'retrieve': PostRetrieveDetailSerializer,
    }


class FlatpageViewSet(AccessViewMixin, ReadOnlyModelViewSet):
    queryset = Flatpage.objects.filter(is_show=True)
    pagination_class = None
    serializer_class = FlatpageSerializer
