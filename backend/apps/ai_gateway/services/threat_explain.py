from apps.ai_gateway.router import route_prompt


def explain_threat_score(entity_id: str, score: int = 87, signals=None, sensitivity_level: str = 'restricted'):
    signals = signals or ['abnormal movement pattern', 'financial anomaly', 'linked network nodes']
    prompt = (
        'Explain this threat score in human-readable bullet points.\n'
        f'Entity: {entity_id}\nScore: {score}\nSignals: {signals}'
    )
    provider, result = route_prompt(task_type='threat_reasoning', prompt=prompt, sensitivity_level=sensitivity_level)
    return provider, result
