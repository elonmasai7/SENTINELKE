from celery import shared_task


@shared_task
def generate_court_report(report_id: int):
    return {'report_id': report_id, 'status': 'queued'}


@shared_task
def process_redaction_job(job_id: int):
    return {'job_id': job_id, 'status': 'queued'}
