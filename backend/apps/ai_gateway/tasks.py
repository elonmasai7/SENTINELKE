from celery import shared_task


@shared_task
def process_ai_request_log(log_id: int):
    return {'log_id': log_id, 'status': 'recorded'}
