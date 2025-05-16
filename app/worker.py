import os
import time

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')


@celery.task(name='create_long_task', bind=True)
def create_long_task(self):
    progress = 0
    while progress < 100:
        time.sleep(3)
        progress += 10
        self.update_state(state='PROGRESS', meta={'progress': progress})
        print(progress)
