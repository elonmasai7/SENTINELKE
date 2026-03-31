from celery import shared_task


@shared_task
def compute_wallet_clusters(case_id: int):
    return {'case_id': case_id, 'status': 'queued'}
