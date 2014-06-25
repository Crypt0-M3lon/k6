from django.conf.urls import patterns, include, url
from django.contrib import admin
from site_ctf import views
from site_ctf import views_admin
from django.views.defaults import page_not_found
from django.contrib.auth.decorators import login_required

admin.autodiscover()
handler404 = 'templates.404'

admin_patterns = patterns('site_ctf.views_admin',
    url(r'^/?$', 'accueil',name='admin_accueil'),
    url(r'/users$', 'view_users',name='view_users'),
    url(r'/cate$', 'view_cate',name='view_cate'),
    url(r'/validations$', 'view_validations',name='view_validations'),
    url(r'/delete_validation/(?P<validationID>[0-9]+)$', 'delete_validation',name='delete_validation'),
    url(r'/delete_chall/(?P<challID>[0-9]+)$', 'delete_chall',name='delete_chall'),
    url(r'/delete_cate/(?P<cateID>[0-9]+)$', 'delete_cate',name='delete_cate'),
    url(r'/challs$', 'view_challs',name='view_challs'),
    url(r'/add_chall$', 'add_chall',name='add_chall'),
    url(r'/add_cate$', 'add_cate',name='add_cate'),
    url(r'/edit_chall/(?P<challID>[0-9]+)$', 'edit_chall', name='edit_chall'),
    url(r'/edit_user/(?P<userID>[0-9]+)$', 'edit_user', name='edit_user'),
    url(r'/edit_cate/(?P<cateID>[0-9]+)$', 'edit_cate', name='edit_cate'),
    
    )

urlpatterns = patterns('site_ctf.views',
    url(r'^admin', include(admin_patterns)),
    url(r'^$', 'accueil', name='accueil'),
    url(r'^view_user/(?P<userID>[0-9]+)$', 'view_user', name='view_user'),
    url(r'^accueil', 'accueil', name='accueil_'),
    url(r'^challs$', 'challs', name='challs'),
    url(r'^challs/(?P<challID>[0-9]+)$', 'view_chall', name='view_chall'),
    url(r'^scoreboard', 'view_scoreboard', name='scoreboard'),
    url(r'^validation', 'validation', name='validation'),
    url(r'^reglement', 'reglement', name='reglement'),
    url(r'^apropos', 'apropos', name='apropos'),
    url(r'^login', 'login_user', name='login'),
    url(r'^logout', 'logout_user', name='logout'),
    url(r'^register', 'register', name='register'),
    url(r'^activate/(?P<codeID>[a-f0-9]{32})', 'activate', name='activate'),
    )

