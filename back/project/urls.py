from django.conf import settings
from django.contrib import admin
from django.conf.urls import (url, include)
from apps.common import views

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^favicon\.ico$', views.FaviconRedirectView.as_view(), name='favicon'),

    url(r'^api/v1/', include('apps.api.urls', namespace='api_v1')),
    # url(r'^robots\.txt$', views.TemplateView.as_view(template_name='robots.txt')),
    # url(r'^sitemap\.xml', views.TemplateView.as_view(template_name='sitempa.xml')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/redactor/', include('redactor.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = views.handler404
# handler500 = views.handler500
