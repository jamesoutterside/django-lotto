from django.conf.urls import *
import views as core_views


urlpatterns = [
    url(r'^$',core_views.index,name='index'),
]