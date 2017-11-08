from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet
from .serializers import NewsSerializer
from apps.news.models import News


class NewsViewSet(MongoModelViewSet):
    lookup_field = 'id'
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.all()
