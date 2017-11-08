import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('blocktimes')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(packages=['news'])
