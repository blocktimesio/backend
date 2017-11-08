from django.conf.urls import include, url
from rest_framework_mongoengine.routers import DefaultRouter
from .views import NewsViewSet

router = DefaultRouter()

router.register(r'news', NewsViewSet, r'news')

urlpatterns = [
    url(r'^v1/', include(router.urls, namespace='v1')),
]
