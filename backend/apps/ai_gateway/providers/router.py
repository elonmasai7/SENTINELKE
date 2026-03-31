import os

from .claude_provider import ClaudeProvider
from .llama_cpp_provider import LlamaCppProvider
from .openrouter_provider import OpenRouterProvider


class ProviderRouter:
    def __init__(self):
        self.default_provider = os.environ.get('AI_DEFAULT_PROVIDER', 'openrouter')
        self.claude = ClaudeProvider()
        self.openrouter = OpenRouterProvider()
        self.llama = LlamaCppProvider()

    def get(self, provider_name: str):
        providers = {
            'claude': self.claude,
            'openrouter': self.openrouter,
            'llama_cpp': self.llama,
        }
        return providers.get(provider_name, providers[self.default_provider])
