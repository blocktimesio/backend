from django.conf.urls import (url, include)

urlpatterns = [
    url('^/', include('apps.api.publick.urls')),
    url('^admin/', include('apps.api.admin.urls')),
]
