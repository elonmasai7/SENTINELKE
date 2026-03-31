from celery import shared_task


@shared_task
def evaluate_behavioral_profile(user_profile_id: int):
    return {'user_profile_id': user_profile_id, 'status': 'queued'}
