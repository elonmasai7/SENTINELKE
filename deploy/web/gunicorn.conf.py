bind = '0.0.0.0:8000'
workers = 3
worker_class = 'uvicorn.workers.UvicornWorker'
accesslog = '-'
errorlog = '-'
timeout = 120
keepalive = 10
