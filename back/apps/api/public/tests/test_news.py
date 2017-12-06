from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from django_dynamic_fixture import G
from apps.common.base_test import BaseTest
from apps.api.public.serializers import NewsListSerializer
from apps.news.models import News


class NewsViewSetTest(BaseTest):
    url = reverse('api_v1:public:news-list')

    def test_filter_by_created__lte(self):
        now = timezone.now()
        G(News, created=now)
        yesterday = now - timedelta(days=1)
        G(News, created=yesterday)

        filter_params = {
            'created__gte': str(now - timedelta(minutes=20)),
        }
        response = self.client.get(self.url, filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        date = response.json()
        self.assertEqual(date['count'], 1)

    def test_filter_by_created__gte(self):
        now = timezone.now()
        G(News, created=now)
        yesterday = now - timedelta(days=1)
        G(News, created=yesterday)

        filter_params = {
            'created__gte': str(now - timedelta(minutes=20)),
        }
        response = self.client.get(self.url, filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        date = response.json()
        self.assertEqual(date['count'], 1)

    def test_order_by_rank_ask(self):
        G(News, views=100)
        G(News, views=200)

        filter_params = {
            'rank__identifier': '1',
        }
        response = self.client.get(self.url, filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = NewsListSerializer(News.objects.all(), many=True)
        self.assertListEqual(
            list(serializer.data),
            response.json()['results']
        )
