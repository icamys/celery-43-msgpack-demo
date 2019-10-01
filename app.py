from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

app.config_from_object('config')
