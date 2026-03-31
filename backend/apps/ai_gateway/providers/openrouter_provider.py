import json
import os
from urllib import request, error


class OpenRouterProvider:
    def __init__(self):
        self.api_key = os.environ.get('OPENROUTER_API_KEY', '')
        self.model = os.environ.get('OPENROUTER_MODEL', 'openrouter/auto')
        self.endpoint = 'https://openrouter.ai/api/v1/chat/completions'

    def generate_response(self, prompt, model=None, timeout=20, retries=2):
        selected_model = model or self.model
        payload = {
            'model': selected_model,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 1000,
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

        last_error = None
        for _ in range(retries + 1):
            try:
                req = request.Request(self.endpoint, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
                with request.urlopen(req, timeout=timeout) as resp:
                    body = json.loads(resp.read().decode('utf-8'))
                choice = (body.get('choices') or [{}])[0]
                text = (choice.get('message') or {}).get('content', '')
                return {'text': text.strip(), 'raw': body}
            except (error.URLError, error.HTTPError, TimeoutError) as exc:
                last_error = str(exc)
        return {'text': '', 'error': f'openrouter_request_failed: {last_error}'}
