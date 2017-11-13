from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import (NewsViewSet, RankConfigView, SignInView, load_image)

router = DefaultRouter()
router.register(r'news', NewsViewSet, r'news')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^sign-in/?$', SignInView.as_view(), name='user_sign_in'),
    url(r'^config/rank/?$', RankConfigView.as_view(), name='config_rank'),
    url(r'^upload-image/?$', load_image, name='admin_upload_file'),
]
