from django.urls import reverse
from rest_framework import status
from django_dynamic_fixture import G
from apps.common.base_test import BaseTest
from apps.api.public.serializers import PostListSerializer
from apps.post.models import Post


class PostViewSetTest(BaseTest):
    url_list = reverse('api_v1:public:post-list')

    def test_get_list(self):
        for i in range(4):
            G(Post)

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        qset = Post.objects.all()
        date = response.json()

        self.assertEqual(date['count'], qset.count())

        list_data = PostListSerializer(qset, many=True)
        self.assertEqual(date['results'], list(list_data.data))
