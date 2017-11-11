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
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['console', ],
            'propagate': False,
        },
        'notification': {
            'handlers': ['console', ],
            'level': 'ERROR',
            'propagate': False
        },
    },
}
