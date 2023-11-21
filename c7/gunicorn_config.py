import multiprocessing
import os

worker_class = 'sync'  # or gthread, gevent, tornado, eventlet, etc.
bind = '0.0.0.0'
timeout = '600'
workers = 2 * multiprocessing.cpu_count() + 1
accesslog = os.getenv("ACCESS_LOG", "-")
errorlog = os.getenv("ERROR_LOG", "-")
########## You can log these to a specific file as well
# accesslog = '/home/site/wwwroot/gunicorn_access_logs'
# errorlog = '/home/site/wwwroot/gunicorn_error_logs'