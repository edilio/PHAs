from django.conf.urls import url


# from rest_framework import routers

from . import views
from .models import Pha


def get_phas():
    return Pha.objects.all()

pha_info = {
    "queryset": Pha.objects.all(),
    "extra_context": {"pha_list": get_phas},
    "paginate_by": 25,
}


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^ph/$', views.ph, name='ph'),
    url(r'^section8/$', views.section8, name='section8'),
    url(r'^without-website/$', views.without_website, name='withoutwebsite'),
    url(r'^without-email/$', views.without_email, name='withoutemail'),
    url(r'^phas/page(?P<page>[0-9]+)$', views.PhaList.as_view(), pha_info),
]
