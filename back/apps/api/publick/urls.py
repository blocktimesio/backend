from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import (
    DomainViewSet, TagViewSet, NewsViewSet,
    RankConfigView, SignInView, load_image,
    FlatpageViewSet
)

router = DefaultRouter()
router.register(r'tag', TagViewSet, r'news')
router.register(r'domain', DomainViewSet, r'news')
router.register(r'news', NewsViewSet, r'news')
router.register(r'flatpage', FlatpageViewSet, r'flatpage')

urlpatterns = [
    url(r'', include(router.urls)),
]
