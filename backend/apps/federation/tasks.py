from celery import shared_task


@shared_task
def dispatch_federated_query(query_id: int):
    return {'query_id': query_id, 'status': 'queued'}
