from django.conf.urls import (url, include)

urlpatterns = [
    url('^/', include('apps.api.public.urls', namespace='public')),
    url('^admin/', include('apps.api.admin.urls')),
]
