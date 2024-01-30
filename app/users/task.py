# from celery import shared_task

from core.celery import app


# @shared_task
@app.task
def add(x, y):
    return x + y
