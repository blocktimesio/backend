from django.conf.urls import include, url
from rest_framework_mongoengine.routers import DefaultRouter
from .views import (NewsViewSet, RankConfigView)

router = DefaultRouter()

router.register(r'news', NewsViewSet, r'news')

urlpatterns = [
    url(r'^admin/', include(router.urls, namespace='v1')),
    url(r'^admin/config/rank/?$', RankConfigView.as_view(), name='config_rank'),
]
