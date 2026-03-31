from django.utils import timezone

from apps.ai_gateway.router import route_prompt
from apps.collaboration.models import WorkspaceNote
from apps.core.models import Case


def generate_case_brief(case_id: int, sensitivity_level: str):
    case = Case.objects.get(id=case_id)
    notes = list(WorkspaceNote.objects.filter(case=case).order_by('-created_at').values_list('body', flat=True)[:20])

    prompt = (
        'Generate one-page case brief, timeline summary, and legal action recommendation.\n'
        f'Case Number: {case.case_number}\n'
        f'Title: {case.title}\n'
        f'Summary: {case.summary}\n'
        f'Generated At: {timezone.now().isoformat()}\n'
        f'Notes: {notes}'
    )
    provider, result = route_prompt(task_type='legal_brief', prompt=prompt, sensitivity_level=sensitivity_level)
    return provider, result
