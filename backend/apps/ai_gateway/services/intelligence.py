from apps.ai_gateway.router import route_prompt


def summarize_intelligence_report(report_text: str, sensitivity_level: str):
    prompt = (
        'Summarize this intelligence report with sections: executive_summary, key_suspects, '
        'locations, risk_indicators, recommended_actions.\n\n'
        f'Report:\n{report_text}'
    )
    provider, result = route_prompt(task_type='strategic_summary', prompt=prompt, sensitivity_level=sensitivity_level)
    return provider, result
