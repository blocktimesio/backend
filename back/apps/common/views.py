from django.views.generic import (TemplateView, RedirectView)


class HomePageView(TemplateView):
    template_name = 'home.html'


class FaviconRedirectView(RedirectView):
    permanent = True
    url = '/static/favicon/favicon.ico'
