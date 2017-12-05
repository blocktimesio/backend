LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['graylog', 'console'],
        'propagate': True,
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
        'graylog': {
            'level': 'DEBUG',
            'class': 'pygelf.GelfTcpHandler',
            'host': 'graylog',
            'port': 12201,
        },
    },
    'loggers': {
        'django.request': {
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'level': 'WARNING',
        },

        'crawlers': {
            'level': 'INFO',
        },

        'celery.task': {
            'level': 'INFO',
        },
        'celery.worker': {
            'level': 'INFO',
        },
    },
}
