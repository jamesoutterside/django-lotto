from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from registration.backends.simple.views import RegistrationView
from apps.core.registration_forms import RegistrationFormExtra

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls')),
]

# django-registration

# set a different form
if getattr(settings, 'INCLUDE_REGISTER_URL', True):
    urlpatterns += [
        url(r'^accounts/register/$',
            RegistrationView.as_view(form_class=RegistrationFormExtra),
            name='registration_register',
            ),
    ]

# include rest of registration normally
urlpatterns += [
    url(r'^accounts/', include('registration.backends.simple.urls')),  # use simple to avoid emails in local #TODO 2step
]



admin.site.site_header = 'Django Lotto Administration'
