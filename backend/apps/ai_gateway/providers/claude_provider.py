import json
import os
from urllib import request, error


class ClaudeProvider:
    def __init__(self):
        self.api_key = os.environ.get('CLAUDE_API_KEY', '')
        self.model = os.environ.get('CLAUDE_MODEL', 'claude-3-5-sonnet-latest')
        self.endpoint = 'https://api.anthropic.com/v1/messages'

    def generate_response(self, prompt, context=None, system_prompt='You are a secure analytical assistant.', timeout=25, retries=2):
        context = context or {}
        content = prompt
        if context:
            content = f"Context: {json.dumps(context, ensure_ascii=True)}\n\nPrompt: {prompt}"

        payload = {
            'model': self.model,
            'max_tokens': 1000,
            'system': system_prompt,
            'messages': [{'role': 'user', 'content': content}],
        }

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
        }

        last_error = None
        for _ in range(retries + 1):
            try:
                req = request.Request(self.endpoint, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
                with request.urlopen(req, timeout=timeout) as resp:
                    body = json.loads(resp.read().decode('utf-8'))
                text_chunks = body.get('content', [])
                output = ' '.join([chunk.get('text', '') for chunk in text_chunks if isinstance(chunk, dict)])
                return {'text': output.strip(), 'raw': body}
            except (error.URLError, error.HTTPError, TimeoutError) as exc:
                last_error = str(exc)
        return {'text': '', 'error': f'claude_request_failed: {last_error}'}
