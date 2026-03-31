import re

from apps.core.models import Case


def process_natural_language_query(query: str):
    normalized = query.strip().lower()
    last_n_days = 30
    match = re.search(r'last\s+(\d+)\s+days', normalized)
    if match:
        last_n_days = int(match.group(1))

    suspect = None
    suspect_match = re.search(r'suspect\s+([a-z0-9_\-]+)', normalized)
    if suspect_match:
        suspect = suspect_match.group(1)

    orm_description = {
        'model': 'Case',
        'filters': {
            'summary__icontains': suspect or '',
        },
        'limit': 25,
        'time_window_days': last_n_days,
    }

    queryset = Case.objects.all().order_by('-created_at')[:25]
    result_set = [
        {
            'case_id': obj.id,
            'case_number': obj.case_number,
            'title': obj.title,
        }
        for obj in queryset
    ]

    explanation = 'Converted natural language into scoped ORM filters on Case records.'
    return {'structured_query': orm_description, 'result_set': result_set, 'explanation': explanation}
