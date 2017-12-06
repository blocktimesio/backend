from rest_framework import serializers

from apps.flatpage.models import Flatpage
from apps.news.models import News
from apps.post.models import Post


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'slug', 'author', 'created',
            'title', 'views', 'comments',
        ]


class NewsRetrieveDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'slug', 'author', 'created',
            'title', 'text', 'image', 'views', 'comments',
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'image', 'author', 'pub_date',
        ]


class PostRetrieveDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'image', 'author', 'pub_date', 'text'
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class FlatpageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flatpage
        fields = [
            'slug', 'title', 'content'
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
