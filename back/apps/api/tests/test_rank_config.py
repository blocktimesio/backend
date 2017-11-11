from django.urls import reverse
from django_dynamic_fixture import N
from rest_framework import status

from .base_test import BaseTest
from apps.news.models import RankConfig


class RankConfigViewTest(BaseTest):
    url = reverse('api_v1:config_rank')

    def test_update(self):
        self.client.force_login(self.user)

        data = N(RankConfig)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        is_exists = RankConfig.objects.filter(**data).count() == 1
        self.assertTrue(is_exists)
