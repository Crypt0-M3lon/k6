from django.conf.urls import patterns, include, url
from django.contrib import admin
from site_ctf import views
from django.views.defaults import page_not_found

admin.autodiscover()
handler404 = 'site_ctf.templates.404'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'k6.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('site_ctf.urls')),

)
