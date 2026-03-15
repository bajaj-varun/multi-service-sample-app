from celery import Celery
import time

celery_app = Celery('app2_worker', broker='redis://redis.default.svc.cluster.local:6379/2', backend='redis://redis.default.svc.cluster.local:6379/2')

@celery_app.task
def process_app2_task(payload):
    time.sleep(2)
    return f"App2 processed {payload}"
