from rest_framework import serializers

from apps.flatpage.models import Flatpage
from apps.news.models import News
from apps.post.models import Post


class NewsListSerializer(serializers.Serializer):
    class Meta:
        model = News
        fields = [
            'slug', 'author', 'created',
            'title', 'views', 'comments',
        ]


class NewsRetrieveDetailSerializer(serializers.Serializer):
    class Meta:
        model = News
        fields = [
            'slug', 'author', 'created',
            'title', 'text' 'image', 'views', 'comments',
        ]


class PostListSerializer(serializers.Serializer):
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'image', 'author', 'pub_date',
        ]


class PostRetrieveDetailSerializer(serializers.Serializer):
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'image', 'author', 'pub_date', 'text'
        ]


class FlatpageSerializer(serializers.Serializer):
    class Meta:
        model = Flatpage
        fields = [
            'slug', 'title', 'content'
        ]
