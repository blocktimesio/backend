from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import (
    NewsViewSet,
)

router = DefaultRouter()
router.register(r'news', NewsViewSet, r'news')

urlpatterns = [
    url(r'', include(router.urls)),
]
