from celery import shared_task


@shared_task
def transcribe_audio(transcript_id: int):
    return {'transcript_id': transcript_id, 'status': 'queued'}
