from celery import Celery
import time

celery_app = Celery('app1_worker', broker='redis://redis.default.svc.cluster.local:6379/1', backend='redis://redis.default.svc.cluster.local:6379/1')

@celery_app.task
def process_app1_task(payload):
    time.sleep(2)
    return f"App1 processed {payload}"
