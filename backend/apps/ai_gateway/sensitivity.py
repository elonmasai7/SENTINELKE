import re

CLASSIFIED_KEYWORDS = {'top secret', 'classified', 'covert', 'sigint source', 'asset identity'}
WITNESS_PATTERNS = [r'\bWITNESS\s*#?\d+\b', r'\bDOB[:\s]+\d{4}-\d{2}-\d{2}\b']
PII_PATTERNS = [r'\b\d{8,16}\b', r'\b\+?\d{10,15}\b', r'\b[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}\b']


def detect_classified_content(prompt: str) -> bool:
    lower = prompt.lower()
    return any(keyword in lower for keyword in CLASSIFIED_KEYWORDS)


def sanitize_prompt(prompt: str, sensitivity_level: str):
    sanitized = prompt
    for pattern in WITNESS_PATTERNS + PII_PATTERNS:
        sanitized = re.sub(pattern, '[REDACTED]', sanitized, flags=re.IGNORECASE)

    classified_detected = detect_classified_content(prompt) or sensitivity_level == 'classified'
    if classified_detected:
        return sanitized, 'classified', True

    if sensitivity_level == 'restricted':
        return sanitized, 'restricted', False

    return prompt, 'public', False
