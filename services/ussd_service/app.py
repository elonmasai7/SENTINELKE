from __future__ import annotations

import os
from urllib import parse, request

from flask import Flask, Response, jsonify, request as flask_request

app = Flask(__name__)
TARGET_URL = os.environ.get(
    'USSD_TARGET_URL',
    'http://127.0.0.1:8010/api/integrations/ussd/africastalking/',
)


@app.get('/health')
def health() -> Response:
    return jsonify({'status': 'ok', 'target_url': TARGET_URL})


@app.post('/ussd/africastalking')
def africastalking_proxy() -> Response:
    payload = parse.urlencode(flask_request.form or flask_request.json or {}).encode('utf-8')
    upstream = request.Request(
        TARGET_URL,
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST',
    )
    try:
        with request.urlopen(upstream, timeout=15) as response:
            body = response.read()
            content_type = response.headers.get('Content-Type', 'text/plain')
            return Response(body, status=response.status, content_type=content_type)
    except Exception as exc:
        return Response(f'END SentinelKE USSD gateway unavailable: {exc}', status=502, content_type='text/plain')


if __name__ == '__main__':
    host = os.environ.get('USSD_HOST', '0.0.0.0')
    port = int(os.environ.get('USSD_PORT', '8050'))
    app.run(host=host, port=port)
