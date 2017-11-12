from django.conf.urls import include, url
from rest_framework_mongoengine.routers import DefaultRouter
from .views import (NewsViewSet, RankConfigView, SignInView, UploadImageView)

router = DefaultRouter()

router.register(r'news', NewsViewSet, r'news')

urlpatterns = [
    url(r'^sign-in/?$', SignInView.as_view(), name='user_sign_in'),

    url(r'^admin/', include(router.urls)),
    url(r'^admin/upload-image/?$', UploadImageView.as_view(), name='admin_upload_file'),
    url(r'^admin/config/rank/?$', RankConfigView.as_view(), name='config_rank'),
]
