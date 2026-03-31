from typing import Tuple

from .providers.router import ProviderRouter


def select_provider(task_type: str, sensitivity_level: str) -> str:
    if sensitivity_level == 'classified':
        return 'llama_cpp'
    if task_type in {'strategic_summary', 'legal_summary', 'legal_brief', 'threat_reasoning'}:
        return 'claude'
    return 'openrouter'


def route_prompt(task_type: str, prompt: str, sensitivity_level: str) -> Tuple[str, dict]:
    provider_name = select_provider(task_type=task_type, sensitivity_level=sensitivity_level)
    router = ProviderRouter()
    provider = router.get(provider_name)

    if provider_name == 'claude':
        result = provider.generate_response(prompt=prompt, context={'task_type': task_type})
    else:
        result = provider.generate_response(prompt=prompt)

    return provider_name, result
