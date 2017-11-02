from django.conf import settings
from django.contrib import admin
from django.conf.urls import (url, include)
# from django_mongoengine import mongo_admin

urlpatterns = [
    # url(r'^favicon\.ico$', views.FaviconRedirectView.as_view(), name='favicon'),
    # url(r'^robots\.txt$', views.TemplateView.as_view(template_name='robots.txt')),
    # url(r'^sitemap\.xml', views.TemplateView.as_view(template_name='sitempa.xml')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^admin/redactor/', include('redactor.urls')),

        # url(r'^admin/crawler/', include(mongo_admin.site.urls)),
    ]
else:
    urlpatterns += [
        url(r'^admin-secret/', include(admin.site.urls)),
        url(r'^admin-secret/redactor/', include('redactor.urls')),

        # url(r'^admin-secret/crawler/', include(mongo_admin.site.urls)),
    ]

# handler404 = views.handler404
# handler500 = views.handler500
