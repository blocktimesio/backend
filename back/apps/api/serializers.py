from datetime import datetime

from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongoserializers
from apps.news.models import (News, RankConfig)


class NewsSerializer(mongoserializers.DocumentSerializer):
    id = serializers.CharField(read_only=False)
    rank = serializers.SerializerMethodField()
    short_text = serializers.SerializerMethodField()
    time_elapsed = serializers.SerializerMethodField()
    social_data = serializers.SerializerMethodField()

    def get_rank(self, obj: News):
        return round(obj.rank, 4)

    def get_short_text(self, obj: News):
        return obj.short_text

    def get_time_elapsed(self, obj: News):
        return round((datetime.now() - obj.created).seconds / 60, 0)

    def get_social_data(self, obj: News):
        default = {
            'google': 0,
            'facebook': {
                'comment_count': 0,
                'share_count': 0
            },
            'linkedin': 0,
            'pinterest': 0,
            'reddit': {
                'ups': 0,
                'downs': 0
            },

            'views': 0,
            'comments': 0,
        }
        default.update(obj.social)
        return default

    class Meta:
        model = News
        fields = '__all__'


class RankConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankConfig
        fields = '__all__'
