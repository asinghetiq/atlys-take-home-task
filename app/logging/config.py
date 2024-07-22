import logging
import logging.config

def setup_logging():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': 'DEBUG',
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'level': 'INFO',
                'filename': 'app.log',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    })
