from django.conf.urls import *
import views as core_views
import admin_views


urlpatterns = [
    url(r'^enter/(?P<lottery_id>\d+)/$',core_views.entry,name='entry'),
    url(r'^user/$',core_views.user_index,name='user_index'),
    url(r'^passed/$',core_views.passed,name='passed'),
    url(r'^$',core_views.index,name='index'),
]

# custom admin urls
urlpatterns += [
    url(r'^admin/manual/draw/(?P<lottery_id>\d+)/$',admin_views.manual_draw,name='admin_manual_draw'),
]

