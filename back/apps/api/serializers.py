from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongoserializers
from apps.news.models import News


class NewsSerializer(mongoserializers.DocumentSerializer):
    id = serializers.CharField(read_only=False)

    class Meta:
        model = News
        fields = '__all__'
