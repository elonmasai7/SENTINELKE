from django.urls import path

from .views import (
    AICaseBriefView,
    AILogListView,
    AIQueryView,
    AISummarizeView,
    AIThreatExplanationView,
    AIVoiceQueryView,
)

urlpatterns = [
    path('query', AIQueryView.as_view(), name='ai-query'),
    path('summarize', AISummarizeView.as_view(), name='ai-summarize'),
    path('case-brief', AICaseBriefView.as_view(), name='ai-case-brief'),
    path('threat-explanation', AIThreatExplanationView.as_view(), name='ai-threat-explanation'),
    path('voice-query', AIVoiceQueryView.as_view(), name='ai-voice-query'),
    path('logs', AILogListView.as_view(), name='ai-logs'),
]
