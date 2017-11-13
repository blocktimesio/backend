from django.conf.urls import (url, include)

urlpatterns = [
    url('^admin/', include('apps.api.admin.urls')),
]
