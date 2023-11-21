import multiprocessing
import os

worker_class = 'sync'  # or gthread, gevent, tornado, eventlet, etc.
bind = '0.0.0.0:8000'  # "127.0.0.1:8000"
timeout = '600'
workers = 2 * multiprocessing.cpu_count() + 1
accesslog = os.getenv("ACCESS_LOG", "-")
errorlog = os.getenv("ERROR_LOG", "-")

