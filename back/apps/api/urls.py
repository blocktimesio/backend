from django.conf.urls import (url, include)

urlpatterns = [
    url('^public/', include('apps.api.public.urls', namespace='public')),
    url('^admin/', include('apps.api.admin.urls')),
]
