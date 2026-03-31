from celery import shared_task


@shared_task
def generate_case_summary(case_id: int):
    return {'case_id': case_id, 'status': 'queued', 'service': 'summarization'}


@shared_task
def run_synthetic_media_scan(scan_id: int):
    return {'scan_id': scan_id, 'status': 'queued', 'service': 'synthetic_media'}
