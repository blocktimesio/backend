from copy import deepcopy
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.news.models import (Domain, Tag, News, RankConfig)
from apps.flatpage.models import Flatpage
from apps.users.admin import User as UserModel

User = get_user_model()  # type: UserModel


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=False)
    rank = serializers.SerializerMethodField()
    short_text = serializers.SerializerMethodField()
    time_elapsed = serializers.SerializerMethodField()
    social_data = serializers.SerializerMethodField()

    domain = DomainSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    def get_rank(self, obj: News):
        return round(obj.rank, 4)

    def get_short_text(self, obj: News):
        return obj.short_text

    def get_time_elapsed(self, obj: News):
        return round((datetime.now() - obj.created).seconds / 60, 0)

    def get_social_data(self, obj: News):
        default = deepcopy(settings.DEFAULT_SOCIAL_NEWS)
        default.update(obj.social)
        return default

    class Meta:
        model = News
        fields = '__all__'


class RankConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankConfig
        fields = '__all__'


class UserJWTSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        filels = ['type', 'username', 'email']


class FlatpageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flatpage
        fields = ['id', 'slug', 'title', 'content']
