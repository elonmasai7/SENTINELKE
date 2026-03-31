from celery import shared_task


@shared_task
def reconcile_offline_sync(log_id: int):
    return {'log_id': log_id, 'status': 'queued'}
