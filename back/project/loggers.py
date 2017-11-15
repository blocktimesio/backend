from django.conf import settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': [],
    },
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s - %(module)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'django': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'localhost',
            'port': 5000,
            'message_type': 'django',
            'fqdn': False,
            'tags': ['django', 'backend'],
        },
        'celery': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'localhost',
            'port': 5000,
            'message_type': 'django',
            'fqdn': False,
            'tags': ['django', 'celery'],
        },
        'crawlers': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'localhost',
            'port': 5000,
            'message_type': 'django',
            'fqdn': False,
            'tags': ['django', 'celery'],
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['django'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['django'],
            'propagate': False,
        },

        'crawlers': {
            'handlers': ['crawlers'],
            'level': 'INFO',
            'propagate': True
        },

        'celery.task': {
            'handlers': ['celery'],
            'level': 'INFO',
            'propagate': True
        },
        'celery.worker': {
            'handlers': ['celery'],
            'level': 'INFO',
            'propagate': True
        },
    },
}

if settings.DEBUG:
    for name in LOGGING['loggers'].keys():
        LOGGING['loggers'][name]['handlers'].append('console')
