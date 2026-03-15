from celery import Celery
import time

celery_app = Celery('app3_worker', broker='redis://redis.default.svc.cluster.local:6379/3', backend='redis://redis.default.svc.cluster.local:6379/3')

@celery_app.task
def process_app3_task(payload):
    time.sleep(2)
    return f"App3 processed {payload}"
