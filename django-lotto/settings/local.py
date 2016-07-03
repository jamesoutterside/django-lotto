from .base import *


ADMINS = (
    ('James Outterside', 'james.outterside@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django-lotto_test.db',
    }
}

# You might want to use sqlite3 for testing in local as it's much faster.
if IN_TESTING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/django-lotto_test.db',
        }
    }

INSTALLED_APPS += ['debug_toolbar']

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    #'debug_toolbar.panels.settings.SettingsPanel',
    #'debug_toolbar.panels.headers.HeadersPanel',
    #'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    #'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    #'debug_toolbar.panels.templates.TemplatesPanel',
    #'debug_toolbar.panels.cache.CachePanel',
    #'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    #'debug_toolbar.panels.redirects.RedirectsPanel',
]

# log everything on development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO', 
        },
    },
}
