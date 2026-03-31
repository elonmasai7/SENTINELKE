from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='SentinelKE ML Services')


class SummaryRequest(BaseModel):
    text: str


class MediaScanRequest(BaseModel):
    media_ref: str


class TranscriptRequest(BaseModel):
    audio_ref: str
    source_language: str = 'auto'
    target_language: str = 'en'


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/summarize')
def summarize(payload: SummaryRequest):
    text = payload.text.strip()
    short = text[:400]
    return {
        'executive_summary': short,
        'key_entities': [],
        'named_locations': [],
        'action_recommendations': 'Review linked entities and escalate if corroborated by additional sources.',
    }


@app.post('/synthetic-media/scan')
def synthetic_scan(payload: MediaScanRequest):
    return {
        'media_ref': payload.media_ref,
        'authenticity_confidence': 0.72,
        'manipulation_likelihood': 0.28,
        'flagged_regions': [],
        'notes': 'Stub model output. Replace with production detector pipeline.',
    }


@app.post('/speech/transcribe-translate')
def transcribe_translate(payload: TranscriptRequest):
    return {
        'audio_ref': payload.audio_ref,
        'original_transcript': '',
        'translated_transcript': '',
        'confidence_score': 0.0,
        'source_language': payload.source_language,
        'target_language': payload.target_language,
    }
