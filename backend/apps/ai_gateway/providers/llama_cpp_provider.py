import json
import os
from urllib import request, error


class LlamaCppProvider:
    def __init__(self):
        self.url = os.environ.get('LLAMA_CPP_URL', 'http://localhost:8080')
        self.endpoint = f"{self.url.rstrip('/')}/completion"

    def generate_response(self, prompt, n_predict=768, n_ctx=4096, timeout=20, retries=2):
        payload = {
            'prompt': prompt,
            'n_predict': n_predict,
            'n_ctx': n_ctx,
            'temperature': 0.2,
            'stop': ['</s>'],
        }
        headers = {'Content-Type': 'application/json'}

        last_error = None
        for _ in range(retries + 1):
            try:
                req = request.Request(self.endpoint, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
                with request.urlopen(req, timeout=timeout) as resp:
                    body = json.loads(resp.read().decode('utf-8'))
                text = body.get('content', '')
                return {'text': text.strip(), 'raw': body}
            except (error.URLError, error.HTTPError, TimeoutError) as exc:
                last_error = str(exc)
        return {'text': '', 'error': f'llama_cpp_request_failed: {last_error}'}
