from django.conf.urls import *

urlpatterns = patterns('core.views',
    url(r'^$',
        view='index',
        name='index'
    ),
)