from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.views.generic import list_detail
from PHALocator.phas.models import Pha

from django.contrib import admin
admin.autodiscover()



def get_phas():
    return Pha.objects.all()

pha_info = {
    "queryset": Pha.objects.all(),
    "extra_context": {"pha_list" : get_phas},
    "paginate_by": 25,
}


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'phas.views.home', name='home'),
    url(r'^ph/$', 'phas.views.ph', name='ph'),
    url(r'^section8/$', 'phas.views.section8', name='section8'),
    url(r'^withoutwebsite/$', 'phas.views.withoutwebsite', name='withoutwebsite'),
    url(r'^withoutemail/$', 'phas.views.withoutemail', name='withoutemail'),
    url(r'^phas/page(?P<page>[0-9]+)$', list_detail.object_list, pha_info),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^tiny_mce/(?P<path>.*)$','django.views.static.serve',
                    {'document_root' : 'C:/Projects/DJango/tinymce/jscripts/tiny_mce/'}),
    url(r'', include('django.contrib.flatpages.urls')),
)
