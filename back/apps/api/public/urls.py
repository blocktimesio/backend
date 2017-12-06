from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import (
    NewsViewSet, PostViewSet,
FlatpageViewSet
)

router = DefaultRouter()
router.register(r'news', NewsViewSet, r'news')
router.register(r'post', PostViewSet, r'post')
router.register(r'post', FlatpageViewSet, r'flatpage')

urlpatterns = [
    url(r'', include(router.urls)),
]
