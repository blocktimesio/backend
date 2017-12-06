from rest_framework import serializers
from apps.news.models import News


class NewsListSerializer(serializers.Serializer):
    class Meta:
        model = News
        fields = [
            'slug', 'author', 'created',
            'title', 'views', 'comments',
        ]


class RetrieveDetailSerializer(serializers.Serializer):
    class Meta:
        model = News
        fields = [
            'slug', 'author', 'created',
            'title', 'text' 'image', 'views', 'comments',
        ]
