from celery import Celery
from util.transcripts import write_transcript

celery_app = Celery(
    'tasks', # app.import_name,
    backend='redis://localhost:6379', # backend=app.config['CELERY_RESULT_BACKEND'],
    # backend='rpc://',
    broker='redis://localhost:6379', # app.config['CELERY_BROKER_URL'],
)

# class ContextTask(Celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)

# celery_app.Task = ContextTask

# `celery -A your_application.celery worker`
# `celery multi start w1 -A proj -l INFO --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log`
# res = tasks.<METHOD>.delay(*args)
# celery_app.AsyncResult(res.id)

@celery_app.task(ignore_result=True)
def celery_transcript(file_id: int):
    write_transcript(file_id)

if __name__ == '__main__':
    celery_app.start()
