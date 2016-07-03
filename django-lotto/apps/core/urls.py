from django.conf.urls import *
import views as core_views


urlpatterns = [
    url(r'^enter/(?P<lottery_id>\d+)/$',core_views.entry,name='entry'),
    url(r'^$',core_views.index,name='index'),
]